import os
import json
import requests

PLATFORM_URL = os.environ.get('PLATFORM_URL', '')
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
token_url = "https://ussd.api.ushahidi.io/oauth/token/"
token = requests.request("POST", token_url, data=token_payload).text
token = "Bearer {}".format(json.loads(str(token))['access_token'])
# Get All Forms
forms = []
forms_header = {
    'Authorization': token
}
forms_url = "https://ussd.api.ushahidi.io/api/v3/forms"
response = requests.request("GET", forms_url, headers=forms_header).text
response = json.loads(str(response))['results']
for form in response:
    forms.append({"id": form['id'], "name": form['name'].upper()})

# Method to get all Fields from Form using id
def form_attributes(id):
    fields = []
    url = "https://ussd.api.ushahidi.io/api/v3/forms/{}/attributes".format(id)
    querystring = {"order":"asc","orderby":"priority"}
    response = requests.request("GET", url, headers=forms_header, params=querystring).text
    response = json.loads(str(response))['results']
    for field in response:
        fields.append({"label": field['label'].upper(), "key": field['key']})
    return fields