from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import json
import deliver
import MySQL
import darkskyreq
import phonenumbers
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    nowt = datetime.now

    body = str(request.values.get('Body', None))
    
    num = request.values.get('From', None)
    
    command = body.lower().split()[0].replace(':', '')
    resp = MessagingResponse()
    
    num = phonenumbers.parse(num, None)
    num = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)
    
    db = MySQL.Database('users')
    db.execute("SELECT * FROM information")
    
    usr = db.usr(num, 'byPhone')

    def readFeed():
        with open('logs/Feedback.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        return data
    
    if command == "actions" or command == "action":
        resp.message("List of commands:\n\nTime: To set the time of day you would like your weather update respond to the number with \"time\" followed by the time you'd like the message. Include am or pm.\n\nLocation: To change your location respond to the number with \"location\" followed by your new location.\n\nWeather: To get a current weather update reply to the number with \"weather\".\n\nYou can respond to the number with feedback or to get in touch with Delaney Kassab at any time.\n\nTo stop receiving messages at any time just reply STOP.")
    
    elif command == "location":
        location = body.lower().replace('location', '')
        usr.location = location
        w = darkskyreq.Weather(usr.location)
        try:
            address = w.getAddress()
            resp.message("Your new location has been set: "+address)
            db.execute('UPDATE information SET location = %s WHERE phone = %s' % (location, usr.phone))
            db.commit()
        except:
            resp.message("We couldn't find that location. Please type \"location\" followed by a valid location.")

    elif command == "weather":
        deliver.sendWeather(usr.customer_id)
        
    elif command == "time":

        time = str(body.lower().replace('time', '').replace(' ', ''))

        if 'a' in time or 'p' in time:
            if 'm' not in time:
                time += 'm'
            if ':' in time:
                try:
                    t = datetime.strptime(time, "%I:%M%p")
                    db.execute('UPDATE information SET usr_time = %s WHERE phone = %s' % (t.strftime("%H:%M"), phone))
                    resp.message(t.strftime("New time set for %I:%M%p"))
                except Exception as e:
                    print(e)
                    resp.message("Oops, you may have misformatted your time. Please double check the time you sent and reply \"time \" followed by time you would like to set.")
            else:
                try:
                    t = datetime.strptime(time, "%I%p")
                    db.execute('UPDATE information SET usr_time = %s WHERE phone = %s' % (t.strftime("%H:%M"), phone))
                    resp.message(t.strftime("New time set for %I:%M%p"))
                except Exception as e:
                    print(e)
                    resp.message("Oops, you may have misformatted your time. Please double check the time you sent and reply \"time \" followed by the time you would like to set.")
        else:
            resp.message("Make sure you include am or pm. Reply \"time \" followed by the time you would like to set.")
        db.commit()
        
    else:
        msg = "New feedback from %s %s %s: %s" % (usr.first_name, usr.last_name, usr.phone, body)
        deliver.send('8049288208', msg)

        resp.message("Your feedback has been recorded. Thank you!")

        data = readFeed()
        data.append(msg)
        with open('logs/Feedback.json','w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    with open('logs/conversationLog.json', 'a', encoding = 'utf-8') as f:
        conv = 'Message from %s %s %s at ' % (usr.first_name, usr.last_name, usr.phone)+nowt(pytz.timezone('America/New_York')).strftime("%b %d at %I:%M%p:")+body
        json.dump(conv, f, ensure_ascii=False, indent=4)
        f.write('\n')
    return str(resp)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port = 5000)
    #app.run(debug=True)
