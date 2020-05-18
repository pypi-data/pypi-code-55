import json
from reqrest import REST

class RunDeck():
    def __init__(self, url, auth, debug=False):
        self.rest = REST(url, headers=self.create_headers(auth), protocol='http', debug=debug)
        self.debug = debug

    # Combine varibles to form headers
    def create_headers(self, auth_token):
        """Creates headers for REST API Call using config"""
        headers = {
            'Accept': "application/json",
            'X-Rundeck-Auth-Token': auth_token,
            'Content-Type': "application/json"
        }

        return headers
    
    # Check HTTP codes for common errors
    # Allow specifying an expected code for custom use
    def check_http_response(self, status_code, expected_code=None):
        """Checks if response is a expected or a known good response"""
        status_codes = {}
        status_codes[200] = True, 'HTTP 200: OK'
        status_codes[201] = True, 'HTTP 201: Created'
        status_codes[204] = True, 'HTTP 204: Empty Response'
        status_codes[400] = False, 'HTTP 400: Bad Request'
        status_codes[401] = False, 'HTTP 401: Check WSO Credentials'
        status_codes[403] = False, 'HTTP 403: Permission denied'
        status_codes[404] = False, 'HTTP 404: Not found'
        status_codes[406] = True, 'HTTP 406: Not Acceptable'
        status_codes[422] = False, 'HTTP 422: Invalid searchby Parameter'

        if status_code == expected_code:
            return True
        elif status_code in status_codes:
            self.debug_print(status_codes[status_code][1])
            return status_codes[status_code][0]
        else:
            print('Unknown code %s' % status_code)
            return False
        
    def debug_print(self, message):
        """If debugging is enabled print message"""
        if self.debug:
            print(message)
    
    def basic_url(self, url, expected_code=None):
        """Basic REST GET returns [Bool, json/str response, status code]"""
        # Query API
        response = self.rest.get(url)

        # Check response and return validated data
        check = self.check_http_response(response.status_code, expected_code=expected_code)

        if check:
            return True, self.str_to_json(response.text), response.status_code
        else:
            return False, None, response.status_code
    
    def str_to_json(self, string):
        """Tries to convert str to json dict, returns None on failure"""
        try:
            return json.loads(string)
        except json.decoder.JSONDecodeError:
            self.debug_print("Object is not json")
            return string
            
    
    # RunDeck specific functions
    def system_test(self):
        """Basic system test"""
        response = self.basic_url('/api/27/metrics/ping', )
        print()

        if response[0]:
            return response[1] == 'pong\n'

    def system_info(self):
        response = self.basic_url('/api/14/system/info')
        print(response)

        if response[0]:
            return response[1]
        
    def get_projects(self):
        response = self.basic_url('/api/1/projects')

        if response[0]:
            return response[1]
        
    def get_jobs(self, project):
        response = self.basic_url('/api/14/project/%s/jobs' % project)

        if response[0]:
            return response[1]

    def get_running_executions(self, project):
        response = self.basic_url('/api/14/project/%s/executions/running' % project)

        if response[0]:
            return response[1]
