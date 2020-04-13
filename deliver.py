import MySQL
import MMSimage
import msg
from twilio.rest import Client
import os


def sendWeather(customer_id):
    db = MySQL.Database('users')
    usr = db.usr(customer_id)
    number = usr.phone

    media = MMSimage.img(customer_id)
    message = None

    if MySQL.listed(number) == 1:
        welcome = "Thank you for signing up for daily weather updates!\nReply \"actions\" for a list of commands, " \
                  "including how to change your location and set what time you'd like to receive messages each day. " \
                  "Default is 6:30am.\nThis is a class project and feedback is welcome at any time. Just reply to the " \
                  "number with whatever you have to say!\nIf you would like to stop receiving messages just reply " \
                  "stop at any time. "
        send(number, welcome)
        print(welcome)
    # send the message:
    send(number, message, media)
    print(number)
    print(message)

#todo don't add "media" to this if it's not sending an image. it still sends MMS which costs more
def send(num, m=None, media=None):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=m,
        from_='+18647546178',
        media_url=media,
        to="+1" + num
    )

    print(message.sid)
