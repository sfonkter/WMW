import MySQL.py
import msg
from twilio.rest import Client
import os

def sendWeather(customer_id):
    
    db = MySQL.Database('users')
    
    usr = db.usr(customer_id)
    location = usr.location
    number = usr.phone
    fname = usr.first_name
    
    message = msg.msg(location, fname)
    
    if MySQL.listed(number) == 1:
        welcome = "Thank you for signing up for daily weather updates!\nReply \"actions\" for a list of commands, including how to change your location and set what time (coming soon) you'd like to receive messages each day. Default is 6:30am.\nThis is a class project and feedback is welcome at any time. Just reply to the number with whatever you have to say!\nIf you would like to stop receiving messages just reply stop at any time."
        send(number, welcome)
        print (welcome)
    #send the message:
    send(number, message)
    print (number)
    print (message)
    
def send(num, m):
    
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token =os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid,auth_token)
    
    message = client.messages \
                    .create(
                        body=m,
                        from_='+18647546178',
                        to="+1"+num
                        #to='+18049288208'
                    )

    print(message.sid)
    
def sendAll():
    for x in range (0, len(userlist.read())):
        sendWeather(userlist.read()[x]['phone'])