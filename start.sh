export FLASK_APP=~/WMW/run.py
export FLASK_ENV=development
workon
cd ~/WMW
python scheduler.py &
flask run --host '0.0.0.0' &
cd ~/WMW/Weather-Photos
python -m http.server 8000 &
twilio phone-numbers:update "+18647546178" --sms-url="http://64.227.23.86:5000/sms" &