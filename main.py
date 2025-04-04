# Team 'Cheese' CanSat -- Main File
# Read README.md

# Import used libraries
# - Website + Google API
from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_socketio import SocketIO, send, emit

# - Data 
import pandas as  pd
import matplotlib, matplotlib.pyplot as plt
matplotlib.use('agg')
# There was a slight issue that arose from testing on a GitHub Codespace at school, where there wasn't a graphics output
# When running on a machine with a graphics output, despite not displaying, it would throw an error due to being not on the main thread. 
# This forces the library to use the 'agg' backend which can only write to files, and cannot create a graphics output, which 
# Works for our purpose, and doesn't throw an error. 

# - Generic Time
from time import sleep
from datetime import datetime

# Generates a random long string
from os import urandom

# - Used for DataDump
import flightid



# Setup for Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('CREDENTIAL_JSON_HERE', scope) # A Gspread credential JSON will need to be 
## Added, and the file path put here for this program to work.
client = gspread.authorize(credentials)

# Open your sheet by name 
sheet = client.open("CanSAT_Data_Live").sheet1  # Make sure the sheet name matches



# Flight ID generation. 
flightid.init() # Generates the flight ID

def getId(): # Gets the flight ID
    return flightid.get() # Basically a wrapper for get() method in the flightid.py file.
    # I tried this method and it prevents other potential issues. 



#@app.route('/') ## -- Old uneeded code as ref -- 
# def readings():
#     # Fetch the latest row from the sheet
#     rows = sheet.get_all_records()  # Get all records in the sheet
#     latest_reading = rows[-1] if rows else {}  # Get the latest reading (last row)
# 
#     # Pass the latest reading data to the template
#     return render_template('readings.html', latest_reading=latest_reading)
# 
# if __name__ == '__main__':
#     app.run(debug=True)

## Concurrent data variables + list for frame. Both used to store concurrent data but very slightly differently. 
conData = [] 
dataList = []
##  = [0] # Ended up unused. Was originally for a system to allow reloading
##... but as I never continued with that, it became unused.
# However - indAddVal is still used for a single odd reloading check which I didn't want to bypass another way 
ongoing = True


## Sets up the app
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24) # Not actually a secret key as we aren't running on production. 
socketio = SocketIO(app) # Sets up socketio


def getData(): ## Gets data from the sheet
    try:
        rows = sheet.get_all_records() 
        latest_reading = rows[-1] if rows else {}
        return {"index:":0,"temp:":latest_reading['Temp'],"pressure:":latest_reading['Pressure'],"alt:":latest_reading['Altitude'],"humidity:":latest_reading['Humidity']}
    except gspread.exceptions.APIError:
        emit("printerr", "Server Error - API Error - Likely ReadRequests Overlimit. Program on cooldown!")
        changeStatusSatelite("Cooldown")
        changeStatusServer("Cooldown")
        sleep(60) # Test and increase cooldown if neccasary. 
        changeStatusServer("Connected")
        changeStatusSatelite("Connected")
        return getData() # Additional thing as this was the source of the issues with returning null, rather than any other error.
    # If the other except is somehow triggered, the original system should catch it. The cooldown thing is specifically as the only API error I've ran into
    # Is read requests per miniute per user. 
    except:
        emit("printerr", "Other Error in getting data!")


def sendLine(d): ## Sends data to the web
    emit("send-line", d)


def manage(sv): ## Main loop
    ongoing = True
    status = True
    index = sv 
    while ongoing:
        line = getData()
        while line is None: # Ocasionally an error is thrown that I believe derives from gpsread failing
            # And is thrown when I try to assign the index. Hopefully this detects and prevents that.
            ## Appnd. My final fix wasn't actually this, however it is the cooldown system seen above. This is still in place to recover incase a different error occurs, which could be fixed
            ## Via recursion, but it would be nice to know that an error here is occuring. 
            sleep(1)
            emit("printerr", "Somehow, getData() returned 'None'! ")
            line = getData()
        line["index:"] = index
        try:
            if (line["pressure:"] == "force" and line["temp:"] == "force" and line["alt:"] == "force" and line["humidity:"] == "force"): # Force ends the recording of data
                ongoing = False
            elif line["pressure:"] != "" and line["temp:"] != "" and line["alt:"] != "" and line["humidity:"] != "":
                float(line["pressure:"]); float(line["temp:"]); float(line["alt:"]); float(line["humidity:"]) # Throws an error if text is input, which brances to the except ValueError: block 
                if status == False:
                    changeStatusSatelite("Connected")
                    status = True
                index += 1
                series = pd.Series(line)
                dataList.append(series) 
                series = series.to_json()
                conData.append(series)
                sendLine(series) 
            else:
                changeStatusSatelite("Disconnected") # Triggers when one or two values are blank
                status = False
        except ValueError:
            changeStatusSatelite("Disconnected") # Triggers when both values are strings but not 'force'
            status = False
        sleep(1)
    ## Do not use this 
    # frame = pd.DataFrame(dataList)
    # frame.plot(kind='line', x='time:', y='pressure:')
    # plt.savefig(f'static/savedFigures/figure{index}Pressure.png')
    # frame.plot(kind='line', x='time:', y='temp:')
    # plt.savefig(f'static/savedFigures/figure{index}Temperature.png')



## These both change status dashboard on the website. 
def changeStatusServer(data):
    # changeStatusServer is for status updates on the backend here.
    emit("change-status-server", data)
def changeStatusSatelite(data):
    # changeStatusSatelite is for status updates on fetching data from
    # The satelite/sheet
    emit("change-status-satelite", data)


@socketio.on("reqsat") ## Is called by the JS side at first
def requestSatStatus(indAddVal):
    if indAddVal < 0: ## Just here because of a random check I got rid of. 
        indAddVal = 0

    emit("startupid", getId()) ## Logs to the console on the JS. 
    changeStatusSatelite("Connected") 
    try: 
        manage(indAddVal)
    except Exception as error:
        changeStatusServer("Error")
        emit("printerr", str(error)) # Prints any errors in manage() to the JS console. 
        requestSatStatus(indAddVal) # Okay this is a last min addition but hopefully
        # It will allow it to save itself if any error that I am yet to run into happens. 
    changeStatusSatelite("Disconnected")

    # Data management
    frame = pd.DataFrame(dataList)

    # Save as CSV in Datadump
    frame.to_csv(f"datadump/datadump_{getId()}", index=False) 
    with open("datadump/flightlogs.md","a+") as logs:
        logs.write(f"ID: {getId()} -- Logged at: {datetime.now()}\n") 



    # Plot as graph
    try:
        frame.plot(kind='line', x='index:', y='pressure:')
        plt.savefig(f'static/savedFigures/figurePressure.png') 
        frame.plot(kind='line', x='index:', y='temp:')
        plt.savefig(f'static/savedFigures/figureTemperature.png')
        frame.plot(kind='line', x='index:', y='alt:')
        plt.savefig(f'static/savedFigures/figureAltitude.png')
        frame.plot(kind='line', x='index:', y='humidity:')
        plt.savefig(f'static/savedFigures/figureHumidity.png')
    except:
        emit("printerr", "Spreadsheet preventing flight from starting, or less likely - error with plotting!")
    changeStatusSatelite("Finished")
    changeStatusServer("Finished") # Flight ends!

    # Termintates this loop

@socketio.on("reqcon") ## Called by the JS side when the page reloads.
def requestConccurentData():
    sleep(1)
    emit("sendcon", conData)
    

@socketio.on("connect")    ## Called upon initial connection.
def connectHandler():
    changeStatusServer("Connected")
    # May have been planned to do something else, but oh well - it doesn't. 


@app.route("/", methods=["POST", "GET"]) ## Startup
def main():    
    return render_template("web.html")


if __name__ == '__main__': ## Runs the initial app
    socketio.run(app)
    



# -- Ancient Waffling Domain --
# Old ideas that I dumped here before development. 

# Get Data
# Sort Data
# Possible ideas about website?

# The line can be intepreted and displayed
# Then the images and dataframe can be uploaded and sorted






# 
# frame = pd.DataFrame(dataList)
# print(frame)
# frame.plot(kind='line', x='time:', y='pressure:')
# plt.savefig(f'savedFigures/figure{index}Pressure.png')
# frame.plot(kind='line', x='time:', y='temp:')
# plt.savefig(f'savedFigures/figure{index}Temperature.png')
# frame.plot(kind='line', x='time:', y='altitude:')
# plt.savefig(f'savedFigures/figure{index}Altitude.png')

