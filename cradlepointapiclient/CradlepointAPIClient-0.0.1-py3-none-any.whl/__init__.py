from CradlepointAPIClient.api_interface import APIPlugin


class Client(APIPlugin):
    headers = {'Content-Type': 'application/json'}
    base_url = None
    token = None

    def connect(self, x_cp_api_id=None, x_cp_api_key=None, x_ecm_api_id=None, x_ecm_api_key=None):
        check_headers = {x_cp_api_id, x_cp_api_key, x_ecm_api_id, x_ecm_api_key}

        if None not in check_headers:
            headers = {
                'X-CP-API-ID': x_cp_api_id,
                'X-CP-API-KEY': x_cp_api_key,
                'X-ECM-API-ID': x_ecm_api_id,
                'X-ECM-API-KEY': x_ecm_api_key,
                'Content-Type': 'application/json'
            }

            self.headers = headers
            self.base_url = f'https://www.cradlepointecm.com/api/{self.api_version}'
        else:
            raise AttributeError('The X-CP-API-ID, X-CP-API-KEY, X-ECM-API-ID and X-ECM-API-KEY are all required!')

    def disconnect(self):
        self.base_url = None
        self.token = None
        self.headers = None
