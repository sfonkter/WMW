import MySQL
import MMSimage
import msg
from twilio.rest import Client
import os


def sendWeather(customer_id, send_type=None):
    db = MySQL.Database('users')
    usr = db.usr(customer_id)
    number = usr.phone

    # send the message:
    if send_type == 'mms':
        send_mms(number, MMSimage.img(customer_id))
    else:
        send(number, msg.msg(customer_id))
    print(number)


def send(num, m=None):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(body=m,
                from_='+18647546178',
                to="+1" + num
                )
    print(message.sid)


def send_mms(num, media):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(from_='+18647546178',
                media_url=media,
                to="+1" + num
                )

    print(message.sid)
