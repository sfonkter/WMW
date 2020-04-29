export FLASK_APP=~/WMW/run.py
export FLASK_ENV=development
twilio phone-numbers:update "+18647546178" --sms-url="http://64.227.23.86:5000/sms" &
workon
cd ~/WMW/Weather-Photos
python -m http.server 8000 &
cd ~/WMW
python scheduler.py &
flask run --host '0.0.0.0'