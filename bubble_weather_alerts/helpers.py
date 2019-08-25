class Location():
	"""A Location"""
	def __init__(self, zip = 95616):
		self.zip = zip
		self.lat = None
		self.long = None
	
	def getLongLat(self):	
		if ((self.lat is None) and (self.long is None)):
			from geopy.geocoders import Nominatim
			geolocator = Nominatim(user_agent="bubble_weather_alerts")
			location = geolocator.geocode(str(self.zip))
			self.lat = location.latitude
			self.long = location.longitude
		return (self.lat, self.long)
        
class Weather():
    
    def __init__(self, historyDays = 5):
        self.history = {
            'temphigh': None,
            'templow': None,
            'humidity': None
        }
        self.days_api_format = self.daysApi(historyDays)
    
    def daysApi(self,historyDays):
        from datetime import datetime, timedelta
        days = [(datetime.now() - timedelta(days=n)) for n in list(range(1,historyDays + 1))]
        #[YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]
        return [d.strftime("%Y-%m-%d") for d in days]
    
    def getHistory(self):
        import requests
        import sys
        # insert at 1, 0 is the script path (or '' in REPL)
        sys.path.insert(1, './APIs/')
        # REDALERT need check best practice for this, make methods etc 'private' (by convention)
        from apis import dark_sky_api_secret_key
        from apis import dark_sky_api_endpoint
        url = dark_sky_api_endpoint + dark_sky_api_secret_key + self.lat + ',' + self.long + ','
        #response = requests.get("https://swapi.co/api/")