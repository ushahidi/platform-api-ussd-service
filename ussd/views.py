from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .api import *
from .models import Log

# Webhook Listener
@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        usrInput = text.split('*')
        step = len(usrInput)

        Log.objects.create(phone_number=str(phone_number), text=str(text))

        response = ""

        if step == 1:
            # Initial Screen
            response += "CON Welcome to Ushahidi USSD \n"
            # Show all forms on Deployment
            for i, form in enumerate(forms):
                response += "{}. {} \n".format(i+1, form['name'])
        
        if step == 2:
            # Next Screen 
            form_choice = len(usrInput[-1])
            fields = form_attributes(form_choice)
            response += "CON Input Needed \n"
            response += fields[0]
            # @TODO Split Field into Screens and Store 'key': 'inputData'

        return HttpResponse(response)
