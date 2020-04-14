import MySQL
import MMSimage
import msg
from twilio.rest import Client
import os


def sendWeather(customer_id, send_type=None):
    db = MySQL.Database('users')
    usr = db.usr(customer_id)
    number = usr.phone

    if MySQL.listed(number) == 1:
        welcome = "Thank you for signing up for daily weather updates!\nReply \"actions\" for a list of commands, " \
                  "including how to change your location and set what time you'd like to receive messages each day. " \
                  "Default is 6:30am.\nThis is a class project and feedback is welcome at any time. Just reply to the " \
                  "number with whatever you have to say!\nIf you would like to stop receiving messages just reply " \
                  "stop at any time. "
        send(number, welcome)
        print(welcome)

    if send_type == 'mms':
        send_mms(number, MMSimage.img(customer_id))
    else:
        send(number, msg.msg(customer_id))
    # send the message:
    print(number)


def send(num, m=None):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=m,
        from_='+18647546178',
        to="+1" + num
    )


def send_mms(num, media):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        from_='+18647546178',
        media_url=media,
        to="+1" + num
    )

    print(message.sid)
