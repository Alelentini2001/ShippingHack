import webbrowser
import requests
import json
import time
import sys
import math
import random


#GET USER LOCATION
send_url = "http://api.ipstack.com/check?access_key=420842183c2b670d8da092c6717024f0"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']

#RADAR.IO API IMPLEMENTATION
headers = {
    'Authorization': 'prj_test_sk_b5cdcfa075785c7e9712db8ef351e34bbca32c17',
}

#PLACE TO FIND CLOSE TO THE LOCATION OF THE USER

#https://www.google.com/maps/dir/?api=1&origin=Space+Needle+Seattle+WA&destination=Pike+Place+Market+Seattle+WA&travelmode=bicycling

def randomGeo(latitude, longitude, radius):
    y0 = latitude
    x0 = longitude
    rd = radius / 111300

    u = random.randrange(0.0, 1.0)
    v = random.randrange(0.0, 1.0)

    w = rd * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)

    xp = x / math.cos(y0)
 
    new_latitude = y + y0
    new_longitude = xp + x0

    return(new_latitude, new_longitude)

radius = 50000 #5 miles

link = "https://www.google.com/maps/dir/?api=1&origin=&destination=Pike+Place+Market+Seattle+WA&travelmode=bicycling"
index = link.find('origin=')
origin = link[:index] + 'origin=' + str(latitude) + "," + str(longitude) + '&destination='
index2 = origin.find('destination=')
newLatitude, newLongitude = randomGeo(latitude, longitude, radius)
destination = origin + str(newLatitude) + "," + str(newLongitude)
#print(destination)
webbrowser.open(destination)
