#WMW
This is how we'll collaborate and push updates to the live server.

Here's what each script does:

  clothes.py: This is just a dictionary with clothing recommendations. The numbers correspond to the temperature. The program uses the outfit listed under 5 when the temp is in the 50's.
  
  darkskyreq.py: This makes the request to DarkSky to get weather data, as well as geocodes the address (turns an address into longitude and latitude). Have to geocode the address because DarkSky requires coordinates, not street address or City, State. darkskyreq.py is a bit messy and I need to go back and clean it up so it makes sense, but for now it works.
  
  deliver.py: This is what sends the message via Twilio. deliver.sendWeather(customer_id) to send the whole weather message, or deliver.send(phone, message) to just send a message to the specified phone number (sendWeather() uses send() to send the final message).
  
  msg.py: This is what builds the message. It takes the location and asks darkskyreq.py for the local weather. It then just divides the high temp for the day by 10 and rounds. It takes that number and gets the corresponding outfit from clothes.py. So 55/10 = 5.5 rounds up to 6. Gets the outfit under 6 from clothes.py. Very crude and now that we have a everything stable and working this should be one of our main focuses.
  
  MySQL.py: This makes a class from the MySQL database. 
  
  run.py: This is confusing, but it just receives incoming messages. This is where it takes commands such as 'location' or 'time'. This is always running on the virtual machine (digital ocean server).
  
  scheduler.py: This reads the time that the user selected and sends a weather update at that time. Every minute it checks if any users are signed up for that time, and if so, sends them the message. If user didn't dictate a time it defaults to 6:30am.
  
Logs folder:
  Stored here are some logs such as everything that is being sent to the phone number (conversationLog.json), errors (errors.json), and any feedback that's sent to the number (Feedback.json).

Other files:
  numbers.json: This is a list of numbers that we have sent messages to. This is used to decide who to send the welcome message to. If the number is not in numbers.json it will be sent a welcome message then added to the list (so they won't receive the welcome message again).

  receive.sh: Run this on the virtual machine to start WMW. It starts the reqired processes in the background. The process are run.py, scheduler.py, and an ngrok tunnel for the webhook which is used by run.py to wait for incoming messages. 
  
  requirements.txt: This is a list of python packages required to run WMW. This is just ot make it easier to install requirements on your local machine if you're going to contribute. Use pip install -r requirements.txt to insall the required packages. I recommend creating a virtual environment to do this. 
