import re
import csv
import json
import urllib2

BASE_URL = 'http://192.168.39.128/street2coordinates/'

def return_latlong(address, BASE_URL, confidence_threshold=0.75):
    this_url = {'address':address}
    encoded_url = urllib.urlencode(this_url)
    conn = urllib.urlopen(BASE_URL, encoded_url)
    json_out = conn.read()

    parsed_json = json.loads(json_out)
    json_values = parsed_json[parsed_json.keys()[0]]
    if json_values['confidence'] >= confidence_threshold:
        lat_coord = json_values['latitude']
        long_coord = json_values['longitude']
    else:
        lat_coord, long_coord = None, None

    return lat_coord, long_coord

address_list = []
for id, address in enumerate(addresses):
    address_lat, address_long = return_latlong(address, BASE_URL)
    address_list.append((address_lat, address_long))


