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

if __name__ == '__main__':
    unittest.main()