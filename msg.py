import clothes
import darkskyreq
from datetime import datetime, timezone
import pytz
import MySQL


def msg(customer_id):
    db = MySQL.Database('users')
    usr = db.usr(customer_id)
    w = darkskyreq.Weather(usr.location)
    try:
        req = w.getweather()
        address = w.getaddress()
    except:
        return "Location not found. Please enter a valid location."

    tz = pytz.timezone(req.timezone)
    time = int(datetime.now(tz).strftime("%H"))

    if 4 <= time < 12:
        greeting = "Good morning, "
    elif 12 <= time < 17:
        greeting = "Good afternoon, "
    else:
        greeting = "Good evening, "

    hi = int(req.daily.data[0].temperature_max)
    lo = int(req.daily.data[0].temperature_min)
    temperature = int(req.currently.temperature)
    feelsLike = int(req.currently.apparent_temperature)
    CurrentSum = req.currently.summary
    HourlySum = req.hourly.summary
    icon = req.daily.data[0].icon

    hiscale = hi
    if hiscale >= 95:
        hiscale = 90
    if hiscale <= 10:
        hiscale = 10
    tempScale = int(hiscale / 10)

    cond = (greeting + usr.first_name + "! Current conditions in " + address + ": Feels like %s\u00b0F and %s. %s" % (
    feelsLike, CurrentSum.lower(), HourlySum))
    temps = (" The high for today is %s and the low %s." % (hi, lo))
    bot = clothes.wear[tempScale]["bottom"]
    top = clothes.wear[tempScale]["top"]
    jak = clothes.wear[tempScale]["jacket"]
    hed = clothes.wear[tempScale]["head"]

    FinalMsg = cond + temps
    FinalMsg += (" Wear %s and a %s" % (bot, top))

    if jak != None:
        FinalMsg += (", also bring a " + jak)
        if hed != None:
            FinalMsg += (" and a " + hed + ".")
        else:
            FinalMsg += (".")
    else:
        FinalMsg += (".")
    if icon == 'rain' or icon == 'snow' or icon == 'sleet':
        FinalMsg += (" And don't forget an umbrella or rain jacket!")

    return FinalMsg, req.daily.icon
