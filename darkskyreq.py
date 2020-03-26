from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import requests

class Weather:
    def __init__(self, loc):
        self.loc = str(loc)
    
    def getCoords(self):
        response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyBWJVULh7VtUPe6LuG-4wvA4UlBMFT8mbo"%(self.loc.replace(" ","+")))
        try:
            coords = response.json()['results'][0]
            return coords

        except:
            return None
        
    def getWeather(self):
        API_KEY = '08649357df9e3f366bc54ca8911a48b8'
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