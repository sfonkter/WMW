from flask import Flask, request, session, url_for
from twilio.twiml.messaging_response import MessagingResponse
import json
import deliver
import MySQL
import darkskyreq
import phonenumbers
from datetime import datetime
import pytz
import os

SECRET_KEY = os.environ['SURVEY_SECRET_KEY']
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    resp = MessagingResponse()
    
    nowt = datetime.now

    body = str(request.values.get('Body', None))
    num = request.values.get('From', None)
    num = phonenumbers.parse(num, None)
    num = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)
    
    command = body.lower().split()[0].replace(':', '')
    
    db = MySQL.Database('users')
    db.execute("SELECT * FROM information")
    usr = db.usr(num, 'byPhone')
    
    #Responds with a list of actions users can take
    if command == "actions" or command == "action":
        resp.message("List of commands:\n\nTime: To set the time of day you would like your weather update respond to the number with \"time\" followed by the time you'd like the message. Include am or pm.\n\nLocation: To change your location respond to the number with \"location\" followed by your new location.\n\nWeather: To get a current weather update reply to the number with \"weather\".\n\nYou can respond to the number with feedback or to get in touch with Delaney Kassab at any time.\n\nTo stop receiving messages at any time just reply STOP.")
    
    #Changes user's location
    elif command == "location":
        location = body.lower().replace('location', '')
        usr.location = location
        w = darkskyreq.Weather(usr.location)
        try:
            address = w.getAddress()
            tz = w.getWeather().timezone
            resp.message("Your new location has been set: "+address)
            db.execute("UPDATE information SET location = '%s' WHERE customer_id = %s" % (location, usr.customer_id))
            db.execute("UPDATE information SET timezone = '%s' WHERE customer_id = %s" % (tz, usr.customer_id))
            db.commit()
        except:
            resp.message("We couldn't find that location. Please type \"location\" followed by a valid location.")
    
    #Sends current conditions to user
    elif command == "weather":
        deliver.sendWeather(usr.customer_id)

    #Sign up a new user via sms signup
    elif command == 'weathermywardrobe' or 'question_id' in session:
        with open('questions.json', 'r') as f:
            survey = json.load(f)
        if 'question_id' in session:
            resp.redirect(url_for('answer',
                                      question_id=session['question_id']))
        else:
            db.addUsr(num)
            welcome_user(resp.message)
            redirect_to_first_question(resp, survey)
    
    #Changes the time the user receives the message
    elif command == "time":
        time = str(body.lower().replace('time', '').replace(' ', ''))

        if 'a' in time or 'p' in time:
            if 'm' not in time:
                time += 'm'
            if ':' in time:
                try:
                    t = datetime.strptime(time, "%I:%M%p")
                    db.execute("UPDATE information SET usr_time = '%s' WHERE customer_id = %s" % (t.strftime("%H:%M"), usr.customer_id))
                    resp.message(t.strftime("New time set for %I:%M%p"))
                except Exception as e:
                    print(e)
                    resp.message("Oops, you may have misformatted your time. Please double check the time you sent and reply \"time \" followed by time you would like to set.")
            else:
                try:
                    t = datetime.strptime(time, "%I%p")
                    db.execute("UPDATE information SET usr_time = '%s' WHERE customer_id = %s" % (t.strftime("%H:%M"), usr.customer_id))
                    resp.message(t.strftime("New time set for %I:%M%p"))
                except Exception as e:
                    print(e)
                    resp.message("Oops, you may have misformatted your time. Please double check the time you sent and reply \"time \" followed by the time you would like to set.")
        else:
            resp.message("Make sure you include am or pm. Reply \"time \" followed by the time you would like to set.")
        db.commit()
        
    # if none of the above are true (there is no command), assumes the message is feedback and saves it to logs/Feedback.json.
    #Also sends a message to me with the feedback, phone number, and first and last name.
    else:
        msg = "New feedback from %s %s %s: %s" % (usr.first_name, usr.last_name, usr.phone, body)
        deliver.send('8049288208', msg)

        resp.message("Your feedback has been recorded. Thank you!")

        with open('logs/Feedback.json','a', encoding='utf-8') as f:
            json.dump(msg, f, ensure_ascii=False, indent=4)
            f.write("\n")
    
    #logs everything sent to the number in logs/conversationLog.json
    with open('logs/conversationLog.json', 'a', encoding = 'utf-8') as f:
        conv = 'Message from %s %s %s at ' % (usr.first_name, usr.last_name, usr.phone)+nowt(pytz.timezone('America/New_York')).strftime("%b %d at %I:%M%p:")+body
        json.dump(conv, f, ensure_ascii=False, indent=4)
        f.write('\n')
        
    return str(resp)

@app.route('/question/<question_id>')
def question(question_id):
    with open('questions.json', 'r') as f:
        survey = json.load(f)
    question = survey[int(question_id)]
    session['question_id'] = question_id
    return sms_twiml(question)

@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    body = str(request.values.get('Body', None))
    
    num = request.values.get('From', None)
    num = phonenumbers.parse(num, None)
    num = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)
    
    db = MySQL.Database('users')
    
    question_id = int(question_id)
    
    with open('questions.json', 'r') as f:
        survey = json.load(f)
    
    db.addUsr(num, question_id, body)
    try:
        next_question = survey[question_id+1]
        return redirect_twiml(next_question)
    except Exception as e:
        print (e)
        return goodbye_twiml()
    
def goodbye_twiml():
    resp = MessagingResponse()
    num = request.values.get('From', None)
    num = phonenumbers.parse(num, None)
    num = phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)
    
    db = MySQL.Database('users')
    usr = db.usr(num, 'byPhone')
    resp.message("Thank you for signing up for Weather My Wardrobe! To set a time to receive messages reply with 'Time' followed by a time of day. Default is 6:30am.")
    if 'question_id' in session:
        del session['question_id']
    return str(resp)
    
def redirect_twiml(question):
    with open('questions.json', 'r') as f:
        survey = json.load(f)
    resp = MessagingResponse()
    resp.redirect(url=url_for('question', question_id=survey.index(question)),
                      method = 'GET')
    return str(resp)

def sms_twiml(question):
    resp = MessagingResponse()
    resp.message(question)
    return str(resp)

def redirect_to_first_question(resp, survey):
    first_question = survey[0]
    first_question_url = url_for('question', question_id = survey.index(first_question))
    resp.redirect(url=first_question_url, method='GET')
    
def welcome_user(send_function):
    welcome_text = 'Thank you for signing up for weather updates with Weather My Wardrobe! To finish signing up just answer the following questions.'
    send_function(welcome_text)

if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host="0.0.0.0", port = 5000)
    app.run(debug=True)
