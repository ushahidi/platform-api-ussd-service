from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from flask import Flask, request
from api import *
from utils import *
import redis
import os

# Get Ushahidi Deployment
USHAHIDI_DEPLOYMENT = os.environ.get('PLATFORM_API', '').replace('.api', '')
deployment_title = USHAHIDI_DEPLOYMENT.replace(
    'https://', '').replace('.ushahidi.io', '')

# Configure Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = redis.StrictRedis(
    host=redis_host, port=redis_port, db=0, charset="utf-8", decode_responses=True)

# Initialize Redis
redis_db.set('valid_ussd_input', '')

# Sentry Integration
SENTRY_DSN = str(os.environ.get('DSN_CODE', ''))

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

# Initialize Flask App
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
# USSD Requests Handler, usage:
# CON - Response requiring Input
# END - Response ending USSD Session
def ussd_handler():
    if request.method == 'GET':
        return "Hey there, I process majorly POST requests from Africa's Talking USSD"
    elif request.method == 'POST':
        # Get responses Array from Redis
        validUserInput = redis_db.get('valid_ussd_input').split('*')
        # Removes '' from initial validUserInput List
        while '' in validUserInput:
            validUserInput.remove('')
        validStep = len(validUserInput)

        # Gets the POST Request Body
        request_data = request.form
        session_id = request_data['sessionId']
        service_code = request_data['serviceCode']
        phone_number = request_data['phoneNumber']
        ussdTextList = request_data['text'].split('*')
        while '' in ussdTextList:
            ussdTextList.remove('')
        step = len(ussdTextList)

        # Set Initial USSD Reponse
        response = ""

        # USSD Interactions => Inputs + Responses
        if step == 0:
            # Initial Screen - Get and Display Surveys/Forms
            response += "CON Welcome to Ushahidi USSD for {}! \n ".format(
                deployment_title)
            response += "Kindly reply a Survey ID. \n"
            # Show all forms on Deployment
            for i, form in enumerate(forms):
                # +1 is so we Surveys start counting from 1
                response += "{}. {} \n".format(i+1, form['name'])

        # Handles everyother screen on USSD
        if step >= 1:
            print(validUserInput)
            print(ussdTextList)
            try:
                # Screen 1 - Get and Display Fields for Selected Surveys
                # Get the last item (-1)
                # Get the actual Survey ID using -1 from Dict e.g. If 1 then ID=0
                form_id = forms[int(ussdTextList[-1])-1]['id']
            except Exception:
                response = "CON Kindly reply with a valid Survey ID. e.g. 1"
            else:
                fields = form_attributes(form_id)  # **fields**
                response += "CON Survey has the following fields: \n"
                response += "\n".join([field['label'] for field in fields])
                response += "\nEnter 0 to continue or cancel."
                redis_db.append('valid_ussd_input', ussdTextList[-1])

            # Handles Screens afer validStep==1 => User Input Screens based on **fields**
            # Override **response** for every Screen
            if validStep >= 1:
                # Get actual fields index from Screen Step
                index = validStep - 1

                # Check if we've exhausted **fields**
                if len(fields) == index:
                    response = "END Thanks for submitting your response."
                    # Call Function to post USSD reponses for Survey/Form fields input i.e. for screens > 2
                    post_ussd_responses(form_id, fields, validUserInput[2:])
                else:
                    # Get Values for Current Field
                    field = fields[index]
                    label = field['label']
                    options = field['options']
                    help_text = get_help_text(field['type'])
                    response = "CON Enter Value for {} \n".format(label)
                    response += "\n (Help text - {})".format(help_text)
                    # Display field options if available
                    if len(options) > 1:
                        for i, option in enumerate(options):
                            response += "\n {} - {}".format(i+1, option)

        return response


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8080)
