from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import requests
import os


class Weather:
    def __init__(self, loc):
        self.loc = str(loc)

    def getcoords(self):
        google_key = os.environ['GOOGLE_API_KEY']
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (
            self.loc.replace(" ", "+"), google_key))
        try:
            coordinates = response.json()['results'][0]
            return coordinates
        except:
            return None

    def getweather(self):
        api_key = os.environ['DARKSKY_API_KEY']
        darksky = DarkSky(api_key)
        coordinates = self.getcoords()

        geodata = dict()
        geodata['lat'] = coordinates['geometry']['location']['lat']
        geodata['lng'] = coordinates['geometry']['location']['lng']

        latitude = geodata['lat']
        longitude = geodata['lng']
        forecast = darksky.get_forecast(
            latitude, longitude,
            extend=False,  # default `False`
            lang=languages.ENGLISH,  # default `ENGLISH`
            values_units=units.AUTO,  # default `auto`
            exclude=[],  # default `[]`,
            timezone=None  # default None - will be set by DarkSky API automatically
        )
        return forecast

    def getaddress(self):
        coords = self.getcoords()
        city = coords['address_components'][0]['short_name']
        state = coords['address_components'][1]['short_name']
        fulladdress = city + ' ' + state
        return fulladdress
