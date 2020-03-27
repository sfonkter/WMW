workon
cd ~/WMW
twilio phone-numbers:update "+18647546178" --sms-url="http://localhost:5000/sms" &
python run.py &
python scheduler.py &
