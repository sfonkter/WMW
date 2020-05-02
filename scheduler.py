import deliver
import schedule
import time
from datetime import datetime
import pytz
import MySQL
import json


def sched():
    nowt = datetime.now
    db = MySQL.Database('users')
    db.execute("SELECT customer_id FROM information")
    rows = db.fetchall()
    for x in range(0, len(rows)):
        customer_id = rows[x][0]
        usr = db.usr(customer_id)

        if usr.location is None:
            continue

        t = usr.usr_time
        if t is None:
            t = '06:30'
        tz = pytz.timezone(usr.timezone)
        localusrt = str(nowt(tz).strftime("%H:%M"))

        if t == localusrt:
            try:
                deliver.sendWeather(usr.customer_id, 'mms')
            except Exception as e:
                with open('logs/errorsLog.json', 'a', encoding='utf-8') as f:
                    error = nowt(pytz.timezone('America/New_York')).strftime(
                        "%b %d at %I:%M%p: User ID: {} Error: {}".format(usr.customer_id, e))
                    json.dump(error, f, ensure_ascii=False, indent=4)
                    f.write('\n')


schedule.every().minute.at(":00").do(sched)
while True:
    schedule.run_pending()
    time.sleep(1)
