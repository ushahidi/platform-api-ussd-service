import json
from geopy.geocoders import Nominatim

# Returns Help Texts for Input Tye
def get_help_text(type):
    with open('input_types.json') as input_types:
        input_types = json.load(input_types)
        if input_types[type]:
            return input_types[type]
        else:
            return 'Enter a Value'

# Returns [Latitude, Longitude] from entered Location
def get_location_coordinates(location):
    geolocator = Nominatim(user_agent="ussd_service")
    location = geolocator.geocode(location)
    if location.address:
        return [location.latitude, location.longitude]
    else:
        return []