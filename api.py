import os
import json
import requests
from utils import *
from datetime import datetime
from requests.exceptions import HTTPError

PLATFORM_API = os.environ.get('PLATFORM_API', '')
EMAIL = os.environ.get('PLATFORM_EMAIL', '')
PASSWORD = os.environ.get('PLATFORM_PASSWORD', '')

# Get Token
token_payload = {
    'username': EMAIL,
    'password': PASSWORD,
    'client_id': 'ushahidiui',
    'client_secret': '35e7f0bca957836d05ca0492211b0ac707671261',
    'scope': '*',
    'grant_type': 'password'
}
token_url = "{}/oauth/token/".format(PLATFORM_API)
token = requests.request("POST", token_url, data=token_payload).text
token = "Bearer {}".format(json.loads(str(token))['access_token'])
# Get All Forms
forms = []
forms_header = {
    'Authorization': token
}
forms_url = "{}/api/v3/forms".format(PLATFORM_API)
response = requests.request("GET", forms_url, headers=forms_header).text
response = json.loads(str(response))['results']
for form in response:
    forms.append({"id": form['id'], "name": form['name'].upper()})

# Method to get all Fields from Form using id
def form_attributes(id):
    fields = []
    url = "{}/api/v3/forms/{}/attributes".format(PLATFORM_API, id)
    querystring = {"order":"asc","orderby":"priority"}
    response = None
    try:
        response = requests.request("GET", url, headers=forms_header, params=querystring).text
        response.raise_for_status() # Raised only when there is error
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    response = json.loads(str(response))['results']
    for field in response:
        fields.append({"label": field['label'].upper(), "key": field['key'], "type": field['input'], "options": field['options']})
    return fields

# Method to post USSD reponses to Ushahidi Dashboard - accepts Survey ID, Fields Array and User Inputs from USSD
def post_ussd_responses(id, fields, ussd_responses):
    # Build post payload
    payload = {
        'title': '',
        'content': '',
        'locale': 'en_US',
        'values': {},
        'post_date': datetime.now().strftime('%Y-%m-%d %H:%M:%SZ'),
        'form': {
            'id': id
        }
    }
    for i, field in enumerate(fields):
        # Set Title & Content values to ussd_responses 0 and 1 respectively
        if i==0:
            payload['title'] = ussd_responses[i]
        elif i==1:
            payload['content'] = ussd_responses[i]
        else:
            # Loop through remaining fields, get the key and corresponding ussd_responses
            key = field['key']
            payload['values'][key] = ussd_responses[i].split(',') # Convert response into Array

            # Modify Special Fields - Override Response Values

            # Set Location Coordinates
            if (fields[i]['type'] == 'location'):
                coordinates = get_location_coordinates(ussd_responses[i]) # Geocode User Location
                payload['values'][key] = [{
                    'lat': coordinates[0],
                    'lon': coordinates[1]
                }]
            # Set Datetime values
            elif (fields[i]['type'] == 'date') or (fields[i]['type'] == 'datetime'):
                datetime_string = ussd_responses[i]
                datetime_object = datetime.strptime(datetime_string, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%SZ')
                payload['values'][key] = datetime_object.split(',')
            # Set Actual Values from Multichoices
            elif (fields[i]['type'] == 'select') or (fields[i]['type'] == 'radio') or (fields[i]['type'] == 'checkbox'):
                selected_choice = ussd_responses[i].split(',') # Numbers from USSD e.g. 1,2
                choice_values = []
                for choice in selected_choice:
                    choice = int(choice) - 1 # Get Actual Index for Option
                    choice_values.append(fields[i]['options'][choice])
                payload['values'][key] = choice_values

    # Make Post request to Submit data
    payload = json.dumps(payload)
    post_url = "{}/api/v3/posts".format(PLATFORM_API)
    try:
        requests.request("POST", post_url, data=payload, headers=forms_header)
        response.raise_for_status() # Raised only when there is error
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print(payload)
