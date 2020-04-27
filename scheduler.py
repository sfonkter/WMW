import deliver
import schedule
import time
from datetime import datetime
import pytz
import MySQL


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
            deliver.sendWeather(usr.customer_id, 'mms')


schedule.every().minute.at(":00").do(sched)
while True:
    schedule.run_pending()
    time.sleep(1)
