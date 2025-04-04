# Red CanSat 2024/25
This is the Rednock School 2024/25 CanSat Repository

**This code is not expected to work. All API keys have been removed - as they were contained in now gitignored credential JSON files. It serves as a demonstration of what we have completed and content to be used by future teams rather than a template.**

No names have been included in this repository, however videos and images of the launch have been, not showing any students or Rednock staff in an identifiable way (There might have been one or two legs or ankles in a shot). 

This is the README.md file of the repository, which means it contains most of the details that you'll need to know. I've split it into four sections:
- An overview of the teams
- A technical overview of all the files
- A review of launch day, 04/04/2025
- A non technical overview of the files, for those who are interested but don't understand my technical overview. 

***
## Teams
There were two teams participating this year with Rednock, although resources and effort were shared between the two groups. 

**'Cheese'**
<br>My team, to the delight of some, was named 'Cheese' by our outreach and design head. On the day of the launch we had four members:
- Me. I'm keeping to my promise of not putting names in this file  but it's my repository, you can check who I am. I worked on project management, our two failed design reports, the website system, and most of this repository. 
- Our engineering head, who worked on the can late into the night, and got it to fit together with a bit of sawing, a lot of effort and hours of soldering. He also worked on the code for the transmitter and reciever. 
- Our outreach and design head, who wrote a ton of lists, one risk assessment, designed and doodled on a parachute, and fantastically slept in the sun during the launch. She named the team, and if we're being honest, was in control. 
- Our yagi-antenna holding head, who also did some work on the can's physical and electrical design, but mainly held the antenna during launch.

**The Other Team**
<br>Now I never caught their team name, however they had five members and worked on their own can. I'm not sure what their individual roles were, however perhaps they spent less time messing around with code than we did, as they actually got a new can printed unlike us who had to use an older can, which still managed to work completely fine.

**The Teachers**
<br>And of course, this wouldn't have been possible without the two fantastic members of staff who funded the operation, printed our cans, drove us to the launch site, and managed to not get any of us electrocuted during the entire saga, which I admit was probably harder than it should have been. 

***
## Technical Overview
A short technical overview of the CanSat.
### The stuff not in the repo.
Not everything is inside this repository unfortunately, however all of our code should be availible in some form for future teams if its not found here.

I don't know much about this part, but I've tried. 

**The Cans**
<br>The cans were 3D printed in PLA, one of which was designed and printed this year, and the other of which was designed and printed for last year's CanSat attempt. 

**The Parachutes**
<br> The parachutes were smaller than you'd expect, as they wanted the cans to fall very very fast. The main reason for this was that they really didn't like the idea of the cans drifting out of the COTEC area, and that's probably for a good reason as the MOD like blowing stuff up out there. As you can see above, our can even had an amazing pattern drawn onto it. 

**The Components**
<br>We used Raspberry Pi Picos as the microcontrolers, and although attempts were made to solder the wiring and the Adafruit BME sensor + the RM9x transmitter to a circuitboard thing, but in the end we just superglued it to a breadboard, shoved it in the can, and stuck a small keychain GPS tracker in there. 

We transmitted at 444MHz.

**The Transmitter/Reciever**
The transmitter and reciver used CircuitPython, which means rather than running it in VScode we either ran it natively on the picos or on Thonny IDE. The code for them is not here, but should be avaible on a seperate repository that I believe the person who wrote it is providing for future groups to use.

We used a yagi antenna connected to the reciever to increase the range, which surprisingly worked really well, as it never actually flew out of range. 

### The stuff in the repo
Some files contain additional comments I've added previously which explain the code.

**.gitignore**
<br> Contains a few ignored files, whether due to them being useless, or to censor API keys or student presence. 

**README.md**
<br>Contains an overview of the CanSat and the repository. 

**datadump**
<br> Contains CSV files with basically no useful data, as we never got a chance to thoroughly test before launch, but they were useful during the development phase.

**datadump/datadump.md**
<br> Contains a short explanation of the datadump folder.

**datadump/flightlogs.md**
<br> Contains a list of all the previous runs (does not include the actual launch or any runs testing on launch day) and the time that they were logged, and the flight ID.

**final_data**
<br> Contains the data we collected from our actual launch on 04/04/2025. Four graphs generated by MatPlotLib and a CSV file of the final launch data.

**sheet_management**
<br> Two outdated files for the sheet management part of the code which used a gspread API to append the data to a google spreadsheet. Not the same as the files we used on launch day.

**static**
<br> Contains the resources for the website.

**static/css/styles.css**
<br> The stylesheet for our website. To be completely honest - it's a mess, but it was my first attempt at a proper HTML build and I think I did an... alright job at it.

**static/js/main.js**
<br> An unused JS file, as due to a small technical issue I decided to embed the JS code into web.html.

**static/savedFigures**
<br>Contains the most recent graphs made by MatPlotLib.

**static/webimages**
<br> Contains the images used for the website. Only the slightly dodgy menu button is left in there as both the can image and placeholder image contained students.

**templates/web.html**
<br> The main frontend body of the project. Contains both the website html + the javascript needed for the website to work. Filled with comments explaining most things.

**flightid.py**
<br> A python file which generates a random unique ID each time the program is run to identify flights for a later date.

**main.py**
<br> The main body of the project. Grabs data from the spreadsheet and uses socketio to send it over to the website. The system upon looking back at it is desperately flawed, and I can think of many better ways to do it. 

Ideally if someone was to rewrite the system, they'd get rid of the google sheet idea completely, work out a way for the pico to write to a file, parse the text in that file, and rathher than the mainloop being on the python side, it should be on the JS side, which may even allow the opportunity to host it with no problems if you work out a few of the other issues.

The python libraries I used are as follows:
- os (urandom, path) - For basic file manipulation and generating the flightid
- flask - To run the web application 
- gspread - To manipulate the google spreadsheet
- oauth2client - Google API authorisation
- flask_socketio - Set up socketio / websockets to communicate between the frontend and backend
- pandas - Store data as dataframes to use with MatPlotLib later and to convert to CSV
- matplotlib (pyplot) - Plot our data as graphs to display 
- time - Use the sleep() function to prevent API read request overlimits
- datetime - Log the exact time of certain flights for testing

**test.py**
<br> A file I used to test something. 

In python any non zero number can be treated as 'True' and zero is treated as 'False', which means if num = "1", the expression num != "" and float(num) returns true, while if num = "0", it returns false. The fix for this bug was removing what was basically the float(num) line from the if statement, as it was only there to throw an easily caught error if alphabetic/symbolic characters were passed in.


***
## Launch Day
04/04/2025 was our CanSat launch day and finally after six months we were going to chuck our hard work into the sky and hope nothing exploded.

The regional launch took place at the Cranfield University COTEC site, which I believe is in area 9 of the Salisbury Plain Training Area. In short, it's a place where they explode things. 

We arrived at the site, and checked in, encouraged by a sign that said we'd be prosecuted under the Official Secrets Act if we failed to do so. We were brought up to the tent which would be our basecamp for the day and given a brief safety briefing, which explained that if we find something that looked like an unexploded bomb, (and walked, swam, and quacked like an unexploded bomb) it was probably an unexploded bomb, and that we shoudn't kick it. I guess the duck method really did come in handy. 

It seems like common sense not to kick the bomb, but the safety officer did tell us that he had seen armed police officers do so. Whether that is encouraging in the sense that nothing is likely to explode, or concerning in the sense that our law enforcement feels the need to kick bombs, we moved on and set ourselves up in the tent. After some last miniute bugfixing, a really tense review of our parachute by the official people, and a bit of tape, kevlar wire and standing on the can to get the lid to fit, we were ready to launch. 

A quick note, but I didn't realise this before the launch day - I was under the assumption that the cans were dropped out of the rocket, which would have caused some major force when the parachute caught initially but I was wrong, instead the cans were launched out of the rocket by an explosively charged piston, which caused something like 80gs of force on the poor can. 

Our can was loaded into the second of the five rockets, and our other team loaded their can into the first. <br>
Launch was upon us. 

Now I think it's probably a bit stupid to say this but the rockets were really loud. I don't see how I could have expected otherwise though, but it still surprised me. 

Here's a couple images and videos of the event.
<img src="readme-pictures/rocketsBeingAdjusted.jpg"></img>

This was the launch of the first rocket.
<video controls src="readme-pictures/rocketLaunch1.mp4"></video>

This was the launch of the third or fourth rocket.
<video controls src="readme-pictures/rocketLaunch3or4.mp4"></video>

The first rocket after launch actually blew across backwards towards us, and somehow out of the entire field it could have landed in, decided to hit some power lines which must have really annoyed a few people. I've heard there were some impressive sparks but I didn't see them.

<img src="readme-pictures\rocket-on-powerlines.jpg"></img>

While the rockets were descending, we had to keep our eyes up to not get hit by one of them or the cans. That didn't happen, but it wasn't too farfetched of a possibility, since they launched so close and the wind blew them back towards us. 

After all five rockets were launched, we were allowed to head into the field to look for and recover our cans, with instructions not to touch any of the fallen rockets since they were covered in hydrochloric acid from the launch. We found our can and returned, with some excellent results. 

Here's our graphs. Match them up to the huge spike on altitude to work out when the launch was:
<img src="final_data\figureAltitudeFINAL.png">
<img src="final_data\figureHumidityFINAL.png">
<img src="final_data\figurePressureFINAL.png">
<img src="final_data\figureTemperatureFINAL.png">

For some reason I think the humidity and pressure values graphs are labeled incorrectly. 

I'm not sure how many of the ten teams in our session managed to recieve data, but I don't think they all did - it's unfortunate that due to some reason unknown we couldn't recieve any data from our other team's can, even with the antenna and making sure we adjusted the recieving frequency correctly.

After we recovered our can, impressed ourselves with the pico still being alive, and packed up, we returned to the minibus and had a short lunch break before returning home, sort of successfully. By that, I mean nobody exploded, caught on fire, got electrocuted, drowned, killed by a mallard, and our can sort of worked. 

***
## The non-technical explanation
Our can contained a sensor, which could measure temperature, humidity, pressure and altitude. It contained a small radio transmitter which communicated with our radio reciver and antenna on the ground. The data recieved from this was put into a google spreadsheet, which was then read, and displayed on a website dashboard, which also displayed the graphs after launch, as well as a small 'about' section. 

After each run, data was saved in a special file type called a CSV, which is simply a text file 


***
## Next Year
Although I'm unlikely to be participating in CanSat for the 2026 launch, I want to provide as much beneficial material as possible. 
***
## Want to use this repository?
If you're participating in the CanSat competition, whether from Rednock or not, you can use the stuff in this repositiory. The code will not work, as there aren't any credentials for the google API, however you can take snippets and use them however you want. 

Have fun launching rockets!