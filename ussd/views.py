import os
import json
import requests
import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse

PLATFORM_URL = os.environ.get('PLATFORM_URL', 'PLATFORM_URL NOT AVAILABLE')
EMAIL = os.environ.get('PLATFORM_EMAIL', '')
PASSWORD = os.environ.get('PLATFORM_PASSWORD', '')
AUTH_URL = urllib.parse.urljoin(PLATFORM_URL, '/oauth/token/')
ACCESS_TOKEN = None

def get_access_token():
    payload = {
        'username': EMAIL,
        'password': PASSWORD,
        'client_id': 'ushahidiui',
        'client_secret': '35e7f0bca957836d05ca0492211b0ac707671261',
        'scope': '*',
        'grant_type': 'password'
    }
    headers = {
    'Content-Type': "application/json",
    }
    return requests.request('POST', AUTH_URL, data=json.dumps(payload), headers=headers)   

def index(request):
    access_token = get_access_token()
    ACCESS_TOKEN = access_token
    return HttpResponse(ACCESS_TOKEN, content_type='text/plain')