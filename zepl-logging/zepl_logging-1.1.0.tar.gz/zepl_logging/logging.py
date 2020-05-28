from datetime import datetime
import requests


class Logging():
    def __init__(self):
        self.url = 'http://zepl.live:8000/logs/'
        self.token = ''
        self.notebook = ''
        self.organization = ''



    def base_config(self, token, notebook='default', organization='default'):
        self.token = token
        self.notebook = notebook
        self.organization = organization

    def info(self, message):
        myobj = {
        'log_type': 'info',
        'message': message,
        'organization': self.organization,
        'notebook': self.notebook,
        'notebook_time': datetime.now()
        }
        headers = {"Authorization": f"Token {self.token}"}

        return str(requests.post(self.url, data = myobj, headers=headers))

    def debug(self, message):
        myobj = {
        'log_type': 'debug',
        'message': message,
        'organization': self.organization,
        'notebook': self.notebook,
        'notebook_time': datetime.now()
        }
        headers = {"Authorization": f"Token {self.token}"}

        return str(requests.post(self.url, data = myobj, headers=headers))

    def warning(self, message):
        myobj = {
        'log_type': 'warning',
        'message': message,
        'organization': self.organization,
        'notebook': self.notebook,
        'notebook_time': datetime.now()
        }
        headers = {"Authorization": f"Token {self.token}"}

        return str(requests.post(self.url, data = myobj, headers=headers))

    def error(self, message):
        myobj = {
        'log_type': 'error',
        'message': message,
        'organization': self.organization,
        'notebook': self.notebook,
        'notebook_time': datetime.now()
        }
        headers = {"Authorization": f"Token {self.token}"}

        return str(requests.post(self.url, data = myobj, headers=headers))

    def critical(self, message):
        myobj = {
        'log_type': 'critical',
        'message': message,
        'organization': self.organization,
        'notebook': self.notebook,
        'notebook_time': datetime.now()
        }
        headers = {"Authorization": f"Token {self.token}"}

        return str(requests.post(self.url, data = myobj, headers=headers))
