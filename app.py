from flask import Flask, request
from api import *

## Sentry Integration
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

SENTRY_DSN = str(os.environ.get('DSN_CODE', ''))

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)

@app.route('/ussd/', methods=['GET', 'POST'])
def ussd_handler():
    # USSD Requests Handler                                                                                                                                                                                                                                                         
    if request.method == 'POST':
        request_data = request.form
        session_id = request_data['sessionId']
        service_code = request_data['serviceCode']
        phone_number = request_data['phoneNumber']
        text = request_data['text']
        usrInput = text.split('*')
        # Remove '' from initial usrInput List
        while '' in usrInput:
            usrInput.remove('')
        step = len(usrInput)
        field = None

        response = ""

        if step == 0:
            # Initial Screen - Get and Display Forms
            response += "CON Welcome to Ushahidi USSD! \n Kindly reply with form ID. \n"
            # Show all forms on Deployment                                                                                                                                                                                                                                                                  
            for i, form in enumerate(forms):
                response += "{}. {} \n".format(i+1, form['name'])
        
        if step >= 1:
            # Next Screen - Get & Display Form Fields to be Inputted
            form_choice = int(usrInput[0])  # Get the Form Choice
            form_id = forms[form_choice-1]['id'] # Get the actual form ID from Dict
            fields = form_attributes(form_id)
            response += "CON You'll be required to enter the following: \n"
            response += "\n".join([ field['label'] for field in fields])
            response += "\nEnter 0 to continue or cancel."
            
            if step > 1:
                index = step - 2

                if len(fields) == index :
                    response = "END Thanks for submitting your response."
                    # @TODO: Send Fields Dict with Response back to API Function for Posting
                else:
                    response = "CON Enter Value for {} \n".format(fields[index]['label'])
                    # @TODO: Attached Response to Fields Dicts.


        return response

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=8080)