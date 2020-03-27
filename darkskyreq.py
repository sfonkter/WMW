from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import requests
import os

class Weather:
    def __init__(self, loc):
        self.loc = str(loc)
    
    def getCoords(self):
        google_key = os.environ['GOOGLE_API_KEY']
        print (google_key)
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s"%(self.loc.replace(" ","+")), google_key)
        print(response)
        try:
            coords = response.json()['results'][0]
            return coords

        except:
            return None
        
    def getWeather(self):
        API_KEY = os.environ['DARKSKY_API_KEY']
        print (API_KEY)
        darksky = DarkSky(API_KEY)
        coords = self.getCoords()
        
        geodata = dict()
        geodata['lat'] = coords['geometry']['location']['lat']
        geodata['lng'] = coords['geometry']['location']['lng']
        
        latitude = geodata['lat']
        longitude = geodata['lng']
        forecast = darksky.get_forecast(
            latitude, longitude,
            extend=False, # default `False`
            lang=languages.ENGLISH, # default `ENGLISH`
            values_units=units.AUTO, # default `auto`
            exclude=[], # default `[]`,
            timezone=None # default None - will be set by DarkSky API automatically
            )
        return forecast
    
    def getAddress(self):
        coords = self.getCoords()
        city = coords['address_components'][0]['short_name']
        state = coords['address_components'][1]['short_name']
        fullAddress = city+' '+state
        return fullAddress