from geopy.geocoders import Nominatim
import validators

# Returns Help Texts for Input Tye
def get_help_text(type):
    input_types = {
        "text": "Enter text",
        "textarea": "Enter longer text",
        "location": "Enter Complete Address",
        "number": "Enter a number",
        "date": "Enter date e.g: 2019-12-31",
        "datetime": "Enter a datetime e.g: 2019-12-31 17:55",
        "select": "Enter the Number for Choice e.g: 1",
        "radio": "Enter the Number for Choice e.g: 1",
        "checkbox": "Enter the Numbers for Choices e.g: 1,2,3"
    }
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

def validate_input(value, type):
    """ 
        Check if input is valid using Validators
        If valid, return True
        Else, return error message

    """
    if validators.length(value, min=1) != "": # For all values
        return True
    else:
        return "Kindly input a correct value!"
