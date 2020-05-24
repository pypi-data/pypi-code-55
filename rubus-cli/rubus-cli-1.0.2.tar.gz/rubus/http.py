import json
import os


def create_headers() -> dict:
    '''
    Create suitable header for application/json Content-Type, and set the
    RUBUS_SESSION variable as Authorization if it exist. Otherwise the user
    is prompted to login.
    '''
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ['RUBUS_SESSION']
        }
        return headers
    except Exception:
        print(
            'Please, log in and set the RUBUS_SESSION environment variable before using this command.')
        os.sys.exit(0)


def handle_response(json_response):
    '''Display nicely the JSON response received from the Rubus API.'''
    print('\n')
    print(json.dumps(json_response, indent=4, sort_keys=True))
