from flask import Flask, request
from api import *

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
            # Initial Screen - Get Form
            response += "CON Welcome to Ushahidi USSD! \n Kindly reply with form ID. \n"
            # Show all forms on Deployment                                                                                                                                                                                                                                                                  
            for i, form in enumerate(forms):
                response += "{}. {} \n".format(i+1, form['name'])
        
        if step == 1:
            # Next Screen - Get & Display Form Fields
            form_choice = int(usrInput[-1])  # Get the last entered value
            form_id = forms[form_choice-1]['id'] # Get the actual form ID from Dict
            fields = form_attributes(form_id)
            response += "CON You'll be required to enter the following: \n"
            response += "\n".join([ field['label'] for field in fields])
            response += "\nEnter any key to continue or cancel."
        
        return response