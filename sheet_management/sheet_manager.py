import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import time
import os

# Setup for Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('CREDENTIAL_JSON_HERE', scope)
client = gspread.authorize(credentials)
sheet = client.open("CanSAT_Data_Live").sheet1  # Open your sheet by name

# File path where the data is stored
file_path = "data.txt"  # Modify this to your file location

# Regular expression to extract the temperature and pressure
pattern = r"Temp: ([\d\.]+) C, Pressure: ([\d\.]+) hPa" ## Notice: This is incomplete code which was changed before launch!

# Keep track of the last read position in the file
last_pos = 0

while True:
    try:
        # Check if the file has been updated
        with open(file_path, "r") as file:
            # Seek to the last read position
            file.seek(last_pos)

            # Read the new content from the file
            new_lines = file.readlines()

            if new_lines:
                data_to_upload = []

                # Process the new lines
                for line in new_lines:
                    match = re.search(pattern, line)
                    if match:
                        # Extract temperature and pressure from the match groups
                        temp = match.group(1)
                        pressure = match.group(2)
                        # Append the extracted data as a list
                        data_to_upload.append([temp, pressure])

                # Batch upload data to Google Sheets
                if data_to_upload:
                    sheet.append_rows(data_to_upload)

                print("New data uploaded to Google Sheets.")

                # Update the last position in the file
                last_pos = file.tell()

        # Wait before checking the file again (e.g., 5 seconds)
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)  # Wait before retrying in case of error
