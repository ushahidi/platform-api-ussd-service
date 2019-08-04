from flask import Flask, request
from api import *
from utils import *
import redis
import os

# Configure Redis
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = redis.StrictRedis(host=redis_host, port=redis_port, db=0, charset="utf-8", decode_responses=True)

# Get Ushahidi Deployment
USHAHIDI_DEPLOYMENT = os.environ.get('PLATFORM_API', '').replace('.api', '')
deployment_title = USHAHIDI_DEPLOYMENT.replace('https://', '').replace('.ushahidi.io', '')

# Sentry Integration
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Initialize Flask App
app = Flask(__name__)

SENTRY_DSN = str(os.environ.get('DSN_CODE', ''))

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

@app.route('/', methods=['GET', 'POST'])
# USSD Requests Handler
# CON - Response requiring Input
# END - Response ending USSD Session                                                                                                                                                                                                                                                      
def ussd_handler():
    if request.method == 'GET':
        return "Hey there, I process majorly POST requests from Africa's Talking USSD"
    elif request.method == 'POST':
        # Gets the POST Request Body
        request_data = request.form
        session_id = request_data['sessionId']
        service_code = request_data['serviceCode']
        phone_number = request_data['phoneNumber']
        text = request_data['text']
        usrInput = text.split('*')
        # Removes '' from initial usrInput List
        while '' in usrInput:
            usrInput.remove('')
        # Gets the current USSD Stage
        step = len(usrInput)

        response = ""

        if step == 0:
            # Initial Screen - Get and Display Surveys/Forms
            response += "CON Welcome to Ushahidi USSD for {}! \n ".format(deployment_title)
            response += "Kindly reply a Survey ID. \n"
            # Show all forms on Deployment                                                                                                                                                                                                                                                                  
            for i, form in enumerate(forms):
                response += "{}. {} \n".format(i+1, form['name']) # +1 is so we Surveys start counting from 1
        
        # Handles everyother screen on USSD
        elif step >= 1:
            try:
                # Screen 1 - Get and Display Fields for Selected Surveys
                form_id = forms[int(usrInput[0])-1]['id'] # Get the actual Survey ID from Dict e.g. If 1 then ID=0
                redis_db.set('valid_ussd_responses', form_id) # Save correct Form ID to Redis
            except Exception:
                response = "CON Kindly reply with a valid Survey ID. e.g. 1"
            else:
                form_id = redis_db.get('valid_ussd_responses')
                fields = form_attributes(form_id) # **fields**
                response += "CON The selected Survey has the following fields: \n"
                response += "\n".join([ field['label'] for field in fields])
                response += "\nEnter 0 to continue or cancel."
            
            # Handles Screens afer Screen 1 - User Input Screens based on **fields**
            # Override **response** for every Screen
            if step > 1:
                # Get actual fields index from Screen Step
                index = step - 2
                
                # Check if we've exhausted **fields**
                if len(fields) == index :
                    response = "END Thanks for submitting your response."
                    # Call Function to post USSD reponses for Survey/Form fields input i.e. for screens > 2
                    post_ussd_responses(form_id, fields, usrInput[2:])
                else:
                    # Get Values for Current Field
                    field = fields[index]
                    label = field['label']
                    options = field['options']
                    help_text = get_help_text(field['type'])
                    response = "CON Enter Value for {} \n".format(label)
                    response += "\n (Help text - {})".format(help_text)
                    # Display field options if available
                    if len(options)>1:
                        for i, option in enumerate(options):
                            response += "\n {} - {}".format(i+1, option)

        return response

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=8080)