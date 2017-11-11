import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDapVav9IuuP5Jjw3ZnDFBqRsFKXN_XIOw')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
APIresponse = gmaps.directions("Manchester Piccadily",
                                     "Manchester Metropolitan university, uk",
                                     mode="walking",departure_time=now)

paths=[]

for routes in APIresponse:
    #print(routes["overview_polyline"]['points'])
    paths.append(routes["overview_polyline"]['points'])

def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
    index, lat, lng = 0, 0, 0
    coordinates = []
    latitude=[]
    longitude=[]
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lat / 100000.0, lng / 100000.0))
        latitude.append(lat/ 100000.0)
        longitude.append(lng / 100000.0)
        
    return coordinates, latitude, longitude

coordinates=decode_polyline(paths[0])[0]
latitude= decode_polyline(paths[0])[1]
longitude= decode_polyline(paths[0])[2]
print(coordinates)

