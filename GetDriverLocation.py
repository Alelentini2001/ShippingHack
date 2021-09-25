#IMPORT LIBRARIES SESSION --------------------------------------
from haversine import inverse_haversine, Direction
from math import pi
import webbrowser
import requests
import json
import time
import sys
import math
import random



#GET USER LOCATION------------------------------------------------
send_url = "http://api.ipstack.com/check?access_key=420842183c2b670d8da092c6717024f0"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']

#RADAR.IO API IMPLEMENTATION--------------------------------------
headers = {
    'Authorization': 'prj_test_sk_b5cdcfa075785c7e9712db8ef351e34bbca32c17',
}

#https://www.google.com/maps/dir/?api=1&origin=Space+Needle+Seattle+WA&destination=Pike+Place+Market+Seattle+WA&travelmode=bicycling
current_location = (latitude, longitude) # (lat, lon)

#print(inverse_haversine(paris, 32, pi * random.uniform(0.0,pi)))

#link = "https://www.google.com/maps/dir/?api=1&origin=&destination=Pike+Place+Market+Seattle+WA&travelmode=bicycling"
#index = link.find('origin=')
#origin = link[:index] + 'origin=' + str(latitude) + "," + str(longitude) + '&destination='
#index2 = origin.find('destination=')
newLatitude, newLongitude = inverse_haversine(current_location, 32, pi * random.uniform(0.0,pi)) # Finding 32 km west from the user's location
#destination = origin + str(newLatitude) + "," + str(newLongitude)
#print(destination)
#webbrowser.open(destination)
