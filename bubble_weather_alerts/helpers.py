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
        maxtries = 3
        tries = 0
        while ((self.lat is None) and (self.long is None)):
            try:
                from geopy.geocoders import Nominatim
                from math import floor
                geolocator = Nominatim(user_agent="bubble_weather_alerts")
                location = geolocator.geocode(str(self.zip))
                self.lat = self.truncate(location.latitude) #truncate but don't round, Dark Sky was returning different final digita and API doesn't require that much precision
                self.long = self.truncate(location.longitude)

                tries = tries + 1
                if (tries == maxtries):
                    break
            except:
                tries = tries + 1
                if (tries == maxtries):
                    break

        return (self.lat, self.long)

class Weather():

    def __init__(self, zip = 96516, historyDays = 5):
        self.history = {
            'temphigh': None,
            'templow': None,
            'humidity': None
        }
        self.coordinates = Location(zip).getLongLat()
        self.location = {
                'lat': self.coordinates[0],
                'long': self.coordinates[1]
                }
        self.days_api_format = self.daysApi(historyDays)
        self.API = API()

    def daysApi(self,historyDays):
        from datetime import datetime, timedelta
        days = [(datetime.now() - timedelta(days=n)) for n in list(range(1,historyDays + 1))]
        #[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
        return [d.strftime("%Y-%m-%d") for d in days]

    def getForecast(self):
        self.forecast = self.API.getData(self.location, forecast = True)
    def getHistory(self):
        pass


class API():
    """Dark Sky API"""
    def __init__(self):
        # insert at 1, 0 is the script path (or '' in REPL)
        import sys
        sys.path.insert(1, './APIs/')
        # REDALERT need check best practice for this, make methods etc 'private' (by convention)
        from apis import dark_sky_api_secret_key
        from apis import dark_sky_api_endpoint

        self.key = dark_sky_api_secret_key
        self.endpoint = dark_sky_api_endpoint
        self.api_time = 'T00:00:00'
        self.api_exclude = '?exclude=minutely'

    def getData(self, location, day = None, forecast = False):
        import requests
        if (forecast):
            url = self.endpoint + self.key + '/' + str(location['lat']) + ',' + str(location['long']) + ',' + self.api_exclude
        else:
            from datetime import datetime
            if (day is None):
                day = datetime.now().strftime("%Y-%m-%d")      #[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
            url = self.endpoint + self.key + '/' + str(location['lat']) + ',' + str(location['long']) + ',' + day + self.api_time + self.api_exclude

        maxtries = 3
        tries = 0
        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                print('Hey what is happening here endless loop...')
                break
            except:
                tries += 1
                if (tries == maxtries):
                    return None
                continue
        return response.json()
