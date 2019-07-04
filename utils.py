import json

# Input Types for Help Texts
def get_help_text(type):
    with open('input_types.json') as input_types:
        input_types = json.load(input_types)
        if input_types[type]:
            return input_types[type]
        else:
            return 'Enter a Value'