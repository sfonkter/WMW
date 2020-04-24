workon
cd ~/WMW
twilio phone-numbers:update "+18647546178" --sms-url="http://64.227.23.86:5000/sms" &
python run.py &
python scheduler.py &
cd ~/WMW/Weather-Photos
python -m http.server 8000 &
