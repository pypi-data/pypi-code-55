from FMCAPIClient.api_interface import APIPlugin
import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response
from datetime import datetime, timedelta
import inspect


class Client(APIPlugin):
    headers = {'Content-Type': 'application/json'}
    base_url = None
    token = None
    auth = None
    token_expire = None
    token_refresh = None
    token_refresh_count = 0
    domain_uuid = None
    server = None

    def connect(self, url: [str, bytes] = '', username: [str, bytes] = '', password: [str, bytes] = ''):
        self.server = url.strip("/")
        self.auth = HTTPBasicAuth(username, password)
        response = requests.post(f'{self.server}/api/fmc_platform/{self.api_version}/auth/generatetoken',
                                 headers=self.headers, auth=self.auth, verify=self.verify)
        if response.status_code == 204:
            self.domain_uuid = response.headers.get('DOMAIN_UUID')
            self.token = response.headers.get('X-auth-access-token')
            self.token_refresh = response.headers.get('X-auth-refresh-token')
            self.token_refresh_count = 0
            self.token_expire = datetime.now() + timedelta(minutes=30)
            self.headers.update({'X-auth-access-token': self.token})

        self.base_url = f'{self.server}/api/fmc_config/{self.api_version}/domain/{self.domain_uuid}'
        return response

    def disconnect(self):
        response = requests.post(f'{self.server}/api/fmc_platform/{self.api_version}/auth/revokeaccess',
                                 headers=self.headers, verify=self.verify)
        return response

    def refresh_token_func(self):
        response = requests.post(f'{self.server}/api/fmc_platform/{self.api_version}/auth/refreshtoken',
                                 headers={'Content-Type': 'application/json',
                                          'X-auth-access-token': self.token,
                                          'X-auth-refresh-token': self.token_refresh},
                                 verify=self.verify)

        if response.status_code == 204:
            self.domain_uuid = response.headers.get('DOMAIN_UUID')
            self.token = response.headers.get('X-auth-access-token')
            self.token_refresh = response.headers.get('X-auth-refresh-token')
            self.token_refresh_count += 1
            self.token_expire = datetime.now() + timedelta(minutes=30)
            self.headers.update({'X-auth-access-token': self.token})

        return response

    def validate_token(self):
        """This validate token is only used internal by the class to check the token in memory with
        the token information it has in memory. Is not design check any external tokens."""
        if self.token_refresh_count >= 3:
            response = self.connect(self.server, self.auth.username, self.auth.password)
        elif self.token_expire <= datetime.now():
            response = self.refresh_token_func()
        else:
            response = Response()
            response.status_code = 204

        return response

    def get(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
            **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        self.validate_token()
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def post(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
             **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        self.validate_token()
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def put(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
            **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        self.validate_token()
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def delete(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
               **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        self.validate_token()
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)
