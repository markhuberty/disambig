import re
import csv
import dstk
import time

## NOTE: this address should be reliable, but
## if it fails then need to check the VM
BASE_URL = 'http://192.168.39.128'
dstk_instance = dstk.DSTK({'apiBase': BASE_URL, 'checkVersion':False})

conn = open('/home/markhuberty/sample_addresses.csv', 'rt')
reader = csv.reader(conn)
addresses = []
for row in reader:
    address = re.sub('"', '', row[0])
    address = re.sub("\\'", '', address)
    addresses.append(address)
conn.close()


def dstk_geocode_options(geo, api_instance):
    """
    Try to geocode, first looking for street (more specific)
    and then place. 
    """
    out = api_instance.street2coordinates(geo)

    if out[geo]:
        return({'street':out[geo]})
    else:
        out = api_instance.text2places(geo)
        if out:
            return({'place':out[0]})
        else:
            return None
    
    

def return_latlong(address,
                   dstkinstance,
                   confidence_threshold=0.75
                   ):
    """
    Returns lat/long of a geocoded address if (1) it can be found in the
    dstk database and (2) (if street) passes the confidence
    threshold
    """
    dstk_out = dstk_geocode_options(address, dstkinstance)
    if dstk_out:
        if 'street' in dstk_out:
            dstk_conf = dstk_out['street']['confidence']

            if dstk_conf >= confidence_threshold:
                lat_coord = dstk_out['street']['latitude']
                long_coord = dstk_out['street']['longitude']
            else:
                lat_coord, long_coord = None, None
        else:
            lat_coord = dstk_out['place']['latitude']
            long_coord = dstk_out['place']['longitude']
    else:
        lat_coord, long_coord = None, None
    return lat_coord, long_coord

address_list = []
t0 = time.time()
for id, address in enumerate(addresses):
    print id
    t1_inc = time.time()
    address_lat, address_long = return_latlong(address,
                                               dstk_instance,
                                               0.7
                                               )
    address_list.append((address_lat, address_long))
t1 = time.time()

## Check the per-instance timing.
time_per = float(t1 - t0) / len(addresses)
print time_per
