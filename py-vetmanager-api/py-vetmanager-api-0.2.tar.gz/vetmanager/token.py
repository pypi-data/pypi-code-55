import requests
from .url import Url


class Login:

    __login: str

    def __init__(self, login: str):
        self.__login = login

    def __str__(self) -> str:
        return self.__login


class Password:

    __password: str

    def __init__(self, password: str):
        self.__password = password

    def __str__(self) -> str:
        return self.__password


class AppName:

    __app_name: str

    def __init__(self, app_name: str):
        self.__app_name = app_name

    def __str__(self) -> str:
        return self.__app_name


class Credentials:

    __login: Login
    __password: Password
    __app_name: AppName
    __credentials_dict: dict

    def __init__(self, login: Login, password: Password, app_name: AppName):
        self.__login = login
        self.__password = password
        self.__app_name = app_name
        self.__credentials_dict = None

    def as_dict(self):
        if self.__credentials_dict is None:
            self.__credentials_dict = dict()
            self.__credentials_dict['login'] = str(self.__login)
            self.__credentials_dict['password'] = str(self.__password)
            self.__credentials_dict['app_name'] = str(self.__app_name)
        return self.__credentials_dict


class Token:

    __url: Url
    __credentials: Credentials
    __saved_token: str

    def __init__(self, url: Url, credentials: Credentials):
        self.__url = url
        self.__credentials = credentials
        self.__saved_token = None

    def __token(self):
        response = requests.post(
            self.__auth_url(),
            data=self.__credentials.as_dict()
        )
        response_json = response.json()
        if response.status_code == 401 or response.status_code == 500:
            raise Exception(response_json['title'])
        return response_json['data']['token']

    def __auth_url(self):
        return self.__url + '/token_auth.php'

    def __str__(self):
        if self.__saved_token is None:
            self.__saved_token = self.__token()
        return self.__saved_token
