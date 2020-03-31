from flask import Flask, request, session, url_for
from twilio.twiml.messaging_response import MessagingResponse
import os
import MySQL
import json

# The session object makes use of a secret key.
SECRET_KEY = os.environ['SURVEY_SECRET_KEY']
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    response = MessagingResponse()
    body = str(request.values.get('Body', None))
    body = 'weathermywardrobe'
    
    if body == 'weathermywardrobe':
        with open('questions.json', 'r') as f:
            survey = json.load(f)
        if 'question_id' in session:
            response.redirect(url_for('answer',
                                      question_id=session['question_id']))
        else:
            welcome_user(survey, response.message)
            redirect_to_first_question(response, survey)
    
    return str(response)

@app.route('/question/<question_id>')
def question(question_id):
    with open('questions.json', 'r') as f:
            survey = json.load(f)
    question = survey[int(question_id)]
    session['question_id'] = question_id
    return sms_twiml(question)

@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):
    with open('questions.json', 'r') as f:
            survey = json.load(f)
    question = survey[question_id]
    next_question = question[question_id+1]
    if next_question:
        return redirect_twiml(next_question)
    else:
        return goodbye_twiml()
    
def redirect_twiml(question):
    with open('questions.json', 'r') as f:
        survey = json.load(f)
    response = MessagingResponse()
    response.redirect(url=url_for('question', question_id=survey.index(question)),
                      method = 'GET')
    return str(response)

def sms_twiml(question):
    response = MessagingResponse()
    response.message(question)
    return str(response)

def redirect_to_first_question(response, survey):
    first_question = survey[0]
    first_question_url = url_for('question', question_id = survey.index(first_question))
    response.redirect(url=first_question_url, method='GET')
    
def welcome_user(survey, send_function):
    welcome_text = 'Thank you for signing up for weather updates with Weather My Wardrobe! To finish signing up just answer the following questions.'
    send_function(welcome_text)

if __name__ == "__main__":
    app.run(debug=True)