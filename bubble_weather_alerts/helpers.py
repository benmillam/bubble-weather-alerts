class Location():
    """A Location"""
    def __init__(self, zip = 95616):
        self.zip = zip
        self.lat = None
        self.long = None
    
    def truncate(self, n, decimals=6):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier
    
    def getLongLat(self):    
        if ((self.lat is None) and (self.long is None)):
            from geopy.geocoders import Nominatim
            from math import floor
            geolocator = Nominatim(user_agent="bubble_weather_alerts")
            location = geolocator.geocode(str(self.zip))
            self.lat = self.truncate(location.latitude) #truncate but don't round, Dark Sky was returning different final digita and API doesn't require that much precision
            self.long = self.truncate(location.longitude)
        return (self.lat, self.long)
        
class Weather():
    
    def __init__(self, zip = 96516, historyDays = 5):
        self.history = {
            'temphigh': None,
            'templow': None,
            'humidity': None
        }
        self.location = Location(zip).getLongLat()
        self.lat = self.location[0]
        self.long = self.location[1]
        self.days_api_format = self.daysApi(historyDays)
    
    def daysApi(self,historyDays):
        from datetime import datetime, timedelta
        days = [(datetime.now() - timedelta(days=n)) for n in list(range(1,historyDays + 1))]
        #[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
        return [d.strftime("%Y-%m-%d") for d in days]
    
    def getDayData(self, day):
        import requests
        import sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, './APIs/')
        # REDALERT need check best practice for this, make methods etc 'private' (by convention)
        from apis import dark_sky_api_secret_key
        from apis import dark_sky_api_endpoint
        api_url_end = 'T12:00:00?exclude=minutely,hourly'
        url = dark_sky_api_endpoint + dark_sky_api_secret_key + '/' + str(self.lat) + ',' + str(self.long) + ',' + day + api_url_end
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def getHistory(self):
        pass
