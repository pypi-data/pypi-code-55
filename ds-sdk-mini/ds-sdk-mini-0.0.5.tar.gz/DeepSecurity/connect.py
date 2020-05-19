#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Connection:
    def __init__(self, config):
        self._config = config
        self._session = None
    def _buildheaders(self):
        return { 'api-secret-key': self._config.api_key,
                               'api-version': 'v1',
                               'Content-Type': 'application/json'}
    def _setupSession(self):
        if self._session is None:
            self._session = requests.Session()
            self._session .headers.update(self._buildheaders())
        return

    def get(self, url, params=None):
        self._setupSession()
        resp = self._session.get(self._config.host + url, verify=self._config.verify_ssl, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content.decode('utf-8'))
        return resp

    def delete(self, url,  params=None):
        self._setupSession()
        resp = self._session.delete(self._config.host + url, verify=self._config.verify_ssl, params=params)
        if resp.status_code == 200:
            return "Success"
        return resp

    def post(self, url, data,  params=None):
        self._setupSession()
        resp = self._session.post(self._config.host + url, verify=self._config.verify_ssl, json=data, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content.decode('utf-8'))
        return resp

    def put(self, url, data,  params=None):
        self._setupSession()
        resp = self._session.put(self._config.host + url, verify=self._config.verify_ssl, json=data, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content.decode('utf-8'))
        return resp