#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import requests
from datetime import datetime
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Connection:
    def __init__(self, config):
        self._config = config
        self._token = None
        self._session = None
        self._loginObject = None
    def _buildheaders(self):
        if self._token:
            return { 'Authorization': "Bearer " +self._token,
                                   'X-Api-Version': '2018-05-01',
                                   'Content-Type': 'application/json'}
        else:
            return {'X-Api-Version': '2018-05-01',
                    'Content-Type': 'application/json'}
    def _setupSession(self):
        if self._session is None:
            self._session = requests.Session()
            if self._token is None:
                self._session.headers.update(self._buildheaders())
                self._GetToken()
            else:
               expires = datetime.strptime(self._loginObject['expires'], "%Y-%m-%dT%H:%M:%SZ")
               if datetime.utcnow() >= expires:
                    self._renewToken()
        return

    def get(self, url, params=None):
        self._setupSession()
        resp = self._session.get(self._config.host + url, verify=self._config.verify_ssl, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content.decode('utf-8'))
        return resp

    def delete(self, url):
        self._setupSession()
        resp = self._session.delete(self._config.host + url, verify=self._config.verify_ssl)
        if resp.status_code == 200:
            return "Success"
        return resp

    def post(self, url, data):
        self._setupSession()
        resp = self._session.post(self._config.host + url, verify=self._config.verify_ssl, json=data)
        if resp.status_code == 200:
            return "Success"
        return resp

    def put(self, url, data):
        self._setupSession()
        resp = self._session.put(self._config.host + url, verify=self._config.verify_ssl, json=data)
        if resp.status_code == 200:
            return "Success"
        return resp


    def _renewToken(self):
        rtv = self._session.post(self._config.host + "/sessions/"+self._loginObject['id'], verify=self._config.verify_ssl)
        if rtv.status_code == 400:
            raise Exception(rtv.text)
        if rtv.status_code == 401:
            raise Exception("Unauthorized: Check your username/password.")
        if rtv.status_code == 200 or rtv.status_code == 201:
            self._loginObject = json.loads(rtv.text)
            self._token = self._loginObject['token']
            self._session.headers.update(self._buildheaders())
        return

    def _GetToken(self):
        loginObject = {
            "user": {
                "userID": self._config.username,
                "password": self._config.password
            }
        }
        rtv = self._session.post(self._config.host  + "/sessions", verify=self._config.verify_ssl, json=loginObject)
        if rtv.status_code == 400:
            raise Exception(rtv.text)
        if rtv.status_code == 401:
            raise Exception("Unauthorized: Check your username/password.")
        if rtv.status_code == 200 or rtv.status_code == 201:
            self._loginObject = json.loads(rtv.text)
            self._token = self._loginObject['token']
            self._session.headers.update(self._buildheaders())
        return