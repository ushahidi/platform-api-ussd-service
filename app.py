from api import *
from utils import *
from setup import *
from store import *


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
        # Gets the POST Request Data
        request_data = request.form
        session_id = request_data['sessionId']
        service_code = request_data['serviceCode']
        phone_number = request_data['phoneNumber']
        ussdTextList = request_data['text'].split('*')

        # Removes '' from list
        while '' in ussdTextList:
            ussdTextList.remove('')
        ussdInputStep = len(ussdTextList)

        # If Redis DB is not empty, get steps and input
        validInputStep = 0
        if redis_db.get(session_id) != None:
            validInputStep = len(redis_db.get(session_id))

        # Set Initial USSD Reponse
        response = ""

        # Initial USSD Screen - Get Survey Choice and save to DB
        if (ussdInputStep >= 0) and (validInputStep == 0):

            if ussdInputStep == 0:
                # Initial Screen - Get and Display Surveys
                response += "CON Welcome to Ushahidi USSD for {}! \n ".format(
                    deployment_title)
                response += "Kindly reply a Survey ID. \n"

                # Show all surveys(forms) on deployment
                for i, survey in enumerate(forms):
                    # +1 is so we Surveys start counting from 1
                    response += "{}. {} \n".format(i+1, survey['name'])

            if ussdInputStep >= 1:
                # Get and Display Fields for Selected Survey if valid
                try:
                    # Tries to get actual survey ID
                    survey_id = forms[int(ussdTextList[-1])-1]['id']
                except Exception:
                    response = "CON Kindly reply with a valid Survey ID. e.g. 1"
                else:
                    # Saves Survey ID and fields to redis DB
                    fields = form_attributes(survey_id)
                    response += "CON Survey has the following fields: \n"
                    response += "\n".join([field['label'] for field in fields])
                    response += "\nEnter 0 to continue or cancel."

                    db_init(session_id)  # Initialize Redis DB
                    db_save(session_id, survey_id)  # Save survey ID
                    db_save(session_id, fields)  # Save survey fields

            return response

        # Further USSD Interactions based on Survey
        # Note that **validUerInput** has 2 entries: survery_id & fields
        if validInputStep >= 2:

            """
                Handles screens for Survey field responses
                Overrides **response** for every new Screen
                Gets the current field's index from ussdInputStep
            """
            index = validInputStep - 2  # Get current index
            validUserInput = db_retrieve(session_id)
            
            print(validUserInput)
            survey_id = int(validUserInput[0])  # Get survey ID
            fields = ast.literal_eval(validUserInput[1])  # Get survey fields

            # Prompt user to input value
            if index < len(fields):
                field = fields[index]
                label = field['label']
                options = field['options']
                help_text = get_help_text(field['type'])
                response = "CON Enter value for {} \n".format(label)
                response += "\n (Help text - {})".format(help_text)

                # Display field options if available
                if len(options) > 1:
                    for i, option in enumerate(options):
                        response += "\n {} - {}".format(i+1, option)

            # Check for input's validity
            if (index >= 0):
                user_input = ussdTextList[-1]
                field_type = fields[index-1]['type']
                validity = validate_input(user_input, field_type)

                if validity:
                    """
                        User input for field is valid based on type
                        Save the input value to our DB - validUserInput
                        User can now go to next screen with next survey field
                    """
                    db_save(session_id, user_input)

                else:
                    # Prompt user to re-input value
                    field = fields[index-1]
                    label = field['label']
                    options = field['options']
                    help_text = get_help_text(field['type'])
                    response = "CON You provided an incorrect input! \n Kindly re-enter a value for {} \n".format(
                        label)
                    response += "\n (Help text - {})".format(help_text)

            # Check if we have exhausted Survey **fields**
            if len(fields) == index:
                response = "END Thanks for submitting your response."
                # Post USSD reponses for Survey fields input
                post_ussd_responses(survey_id, fields, validUserInput[2:])

            return response


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8080)
