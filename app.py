from flask import Flask, request
from api import * # Ushahidi API Requests Modul
import json

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

## Input Types for Help Texts
input_types = None
with open('input_types.json') as input_types:
    input_types = json.load(input_types)

@app.route('/ussd/', methods=['GET', 'POST'])
# USSD Requests Handler
# CON - Response requiring Input
# END - Response ending USSD Session                                                                                                                                                                                                                                                      
def ussd_handler():
    if request.method == 'POST':
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
            response += "CON Welcome to Ushahidi USSD! \n Kindly reply with form ID. \n"
            # Show all forms on Deployment                                                                                                                                                                                                                                                                  
            for i, form in enumerate(forms):
                response += "{}. {} \n".format(i+1, form['name'])
        
        # Handles everyother screen on USSD
        elif step >= 1:
            # Screen 1 - Get and Display Fields for Selected Surveys
            form_choice = int(usrInput[0])  # Get the Survey Choice
            form_id = forms[form_choice-1]['id'] # Get the actual Survey ID from Dict
            fields = form_attributes(form_id) # **fields**
            response += "CON You'll be required to enter the following: \n"
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
                    # @TODO: Send Fields Dict with Response back to API Function for Posting
                else:
                    field = fields[index]
                    response = "CON Enter Value for {} \n".format(field['label'])
                    response += "\n Help text - {}".format(input_types[field['type']])
                    # @TODO: Attached Response to Fields Dicts.


        return response

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=8080)