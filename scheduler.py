import deliver
import schedule
import time
from datetime import datetime, timezone
import pytz
import json
import MySQL


def sched():
    nowt = datetime.now
    db = MySQL.Database('users')
    db.execute("SELECT * FROM information")
    for x in range(1, len(db.fetchall()) + 1):
        if not db.usr(x):
            continue
        else:
            usr = db.usr(x)
        try:
            t = usr.usr_time
            if t == None:
                t = '06:30'
            tz = pytz.timezone(usr.timezone)
            localt = str(nowt(tz).strftime("%H:%M"))

            if t == localt:
                deliver.sendWeather(usr.customer_id, 'mms')

        except Exception as e:
            err = nowt(pytz.timezone('America/New_York')).strftime("%b %d at %I:%M%p: User: {} {} {}: ").format(
                usr.phone, usr.first_name, usr.last_name) + str(e)
            print(err)
            with open('logs/errors.json', 'a', encoding='utf-8') as f:
                json.dump(err, f, ensure_ascii=False, indent=4)
                f.write('\n')


schedule.every().minute.at(":00").do(sched)
while True:
    schedule.run_pending()
    time.sleep(1)
