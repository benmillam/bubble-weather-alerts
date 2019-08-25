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