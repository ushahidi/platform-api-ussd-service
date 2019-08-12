from api import *
from utils import *
from setup import *

@app.route('/', methods=['GET', 'POST'])
def ussd_handler():
    """
        USSD Requests Handler, usage:
        CON - Response requiring Input
        END - Response ending USSD Session
    """
    if request.method == 'GET':
        return "Hey there, I process majorly POST requests from Africa's Talking USSD"
    elif request.method == 'POST':
        # Gets the POST Request Body
        request_data = request.form
        session_id = request_data['sessionId']
        service_code = request_data['serviceCode']
        phone_number = request_data['phoneNumber']
        ussdTextList = request_data['text'].split('*')
        # Removes '' from list
        while '' in ussdTextList:
            ussdTextList.remove('')
        step = len(ussdTextList)

        validStep = 0
        if redis_db.get(session_id) != None:
            validStep = len(redis_db.get(session_id))

        # Set Initial USSD Reponse
        response = ""

        if (step >= 0) and (validStep == 0):

            if step == 0:
                # Initial Screen - Get and Display Surveys/Forms
                response += "CON Welcome to Ushahidi USSD for {}! \n ".format(
                    deployment_title)
                response += "Kindly reply a Survey ID. \n"
                # Show all forms on Deployment
                for i, form in enumerate(forms):
                    # +1 is so we Surveys start counting from 1
                    response += "{}. {} \n".format(i+1, form['name'])

            if step >= 1:
                """
                    Screen 1 - Get and Display Fields for Selected Surveys
                """
                try:
                    form_id = forms[int(ussdTextList[-1])-1]['id']
                except Exception:
                    response = "CON Kindly reply with a valid Survey ID. e.g. 1"
                else:
                    fields = form_attributes(form_id)  # **fields**
                    response += "CON Survey has the following fields: \n"
                    response += "\n".join([field['label'] for field in fields])
                    response += "\nEnter 0 to continue or cancel."
                    # Initialize Redis with unique session_id
                    redis_db.set(session_id, '')
                    redis_db.append(session_id, form_id) # Save form ID
                    redis_db.append(session_id, f"*{str(fields)}") # Save form Fields

            return response

        # Further USSD Interactions
        if len(redis_db.get(session_id)) >= 1:

            """
                Handles screens for User Form Responses
                Override **response** for every Screen
                Get actual fields index from Step
            """
            validUserInput = redis_db.get(session_id).split('*')
            index = len(validUserInput) - 2 # Get current index
            
            form_id = int(validUserInput[0]) # Get saved form id
            fields = ast.literal_eval(validUserInput[1]) # Get saved form fields
            
            # Ask Users to Input responses
            if index < len(fields):
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
            
            # Validity check 
            if (index>=0):
                # Set Value for previous field
                validity = validate_input(ussdTextList[-1], fields[index-1]['type'])
                if validity:
                    redis_db.append(session_id, f"*{ussdTextList[-1]}") # Save response
                else:
                    # Ask user to renter input
                    field = fields[index-1]
                    label = field['label']
                    options = field['options']
                    help_text = get_help_text(field['type'])
                    response = "CON Incorrect Input! \n Kindly re-enter a Value for {} \n".format(label)
                    response += "\n (Help text - {})".format(help_text)
            
            # Check if we've exhausted **fields**
            if len(fields) == index:
                response = "END Thanks for submitting your response."
                # Call Function to post USSD reponses for Survey/Form fields input
                post_ussd_responses(form_id, fields, validUserInput[2:])

            return response


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8080)
