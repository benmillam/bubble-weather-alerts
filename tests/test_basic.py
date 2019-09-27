# -*- coding: utf-8 -*-

from context import bubble_weather_alerts

import unittest

class TestLocationClass(unittest.TestCase):
    """Basic test cases."""

    def test_instantiate_location(self):
        loc = bubble_weather_alerts.helpers.Location()
        self.assertEqual(loc.__class__.__name__, 'Location')

    def test_set_default_zip(self):
        loc = bubble_weather_alerts.helpers.Location() #no zip!
        self.assertEqual(loc.zip,95616)

    def test_setting_zip(self):
        loc = bubble_weather_alerts.helpers.Location(95618) #different zip!
        self.assertEqual(loc.zip,95618)

    def test_get_long_lat_from_zip(self):
        loc = bubble_weather_alerts.helpers.Location()
        self.assertEqual(loc.getLongLat(),(38.547485, -121.738295)) #95616 long lat via https://nominatim.openstreetmap.org/ (actually the website truncates some digits so you ended up pasting the full method result into the test later

    def test_need_call_getLongLat_to_set_attributes(self):
        loc = bubble_weather_alerts.helpers.Location()
        self.assertEqual((loc.lat,loc.long),(None,None)) #getLongLat hasn't set these!

    def test_getLongLat_sets_long_lat_attributes(self):
        loc = bubble_weather_alerts.helpers.Location()
        loc.getLongLat()
        self.assertEqual((loc.lat,loc.long),(38.547485, -121.738295)) #hrmm test isn't independent?

class TestWeatherClass(unittest.TestCase):
    """Basic test cases."""

    def test_instantiate_weather(self):
        weather = bubble_weather_alerts.helpers.Weather()
        self.assertEqual(weather.__class__.__name__, 'Weather')

    def test_need_call_their_methods_to_set_attributes(self):
        weather = bubble_weather_alerts.helpers.Weather()
        self.assertEqual((weather.history['temphigh'],weather.history['templow'],weather.history['humidity']),(None,None, None)) #e.g. getHistory hasn't set these!

    def test_set_list_of_days_formatted_for_Dark_Sky_API(self):
        weather = bubble_weather_alerts.helpers.Weather(historyDays = 7)
        self.assertEqual(len(weather.days_api_format),7)
        self.assertEqual(len(weather.days_api_format[0]),10) #e.g. 2019-07-06, weak but moving on

    def test_instantiate_API_on_Weather(self):
        weather = bubble_weather_alerts.helpers.Weather()
        self.assertEqual(weather.API.__class__.__name__, 'API')

    def test_getForecast_returns_API_data_dict(self):
        weather = bubble_weather_alerts.helpers.Weather(95618)
        weather.getForecast() #sets .forecast property
        assert('latitude' in weather.forecast) #limited coverage here, unexplored edge cases in terms of what API might return unexpectedly

    def test_where_left_off(self):
        #getDayData returns a historical day's weather data, need look through and determine exactly what we'll store like per the next test
        assert(False)

    def test_getHistory_sets_lists(self):
        weather = bubble_weather_alerts.helpers.Weather()
        weather.getHistory()
        self.assertEqual((type(weather.history['temphigh']),type(weather.history['templow']),type(weather.history['humidity'])), (list,list,list))


class TestAPIClass(unittest.TestCase):
    """Basic test cases."""

    def test_instantiate_api(self):
        api = bubble_weather_alerts.helpers.API()
        self.assertEqual(api.__class__.__name__, 'API')

    def test_api_imports_configs(self):
        api = bubble_weather_alerts.helpers.API()
        assert(api.key)
        assert(api.endpoint)

    def test_api_getData_method(self):
        api = bubble_weather_alerts.helpers.API()
        assert(api.getData)

    def test_getData_returns_API_data(self):
        api = bubble_weather_alerts.helpers.API()
        location = {
                'lat': 38.547485,
                'long': -121.738295
                }
        data = api.getData(location, forecast = False)
        assert(data)






if __name__ == '__main__':
    unittest.main()
