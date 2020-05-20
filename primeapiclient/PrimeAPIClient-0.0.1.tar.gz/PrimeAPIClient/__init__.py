from PrimeAPIClient.api_interface import APIPlugin
from base64 import b64encode


class Client(APIPlugin):
    headers = {'Content-Type': 'application/json'}
    base_url = None
    token = None

    def connect(self, url: [str, bytes] = '', username: [str, bytes] = '', password: [str, bytes] = ''):
        self.base_url = f'{url.strip("/")}/webacs/api/{self.api_version}'
        self.token = b64encode(f'{username}:{password}'.encode('UTF-8'))
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Basic {self.token.decode("UTF-8")}'}

    def disconnect(self):
        self.base_url = None
        self.token = None
        self.headers = None
