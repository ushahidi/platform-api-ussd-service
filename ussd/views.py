import os
from django.shortcuts import render
from django.http import HttpResponse

PLATFORM_URL = os.environ.get('PLATFORM_URL', 'PLATFORM_URL NOT AVAILABLE')

def index(request):
    return HttpResponse(PLATFORM_URL, content_type="text/plain")