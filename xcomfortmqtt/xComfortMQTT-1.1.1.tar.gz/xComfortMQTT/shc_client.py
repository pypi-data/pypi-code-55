#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# coding=utf-8
'''
@author: karel.blavka@gmail.com
'''
import json
import requests
import logging


class SHC_Client_Exception(Exception):
    pass


class SHC_Client():

    def __init__(self, host, username, password):
        self._host = host
        self._username = username
        self._password = password
        self._session = requests.Session()
        self._mess_id = None

    def post(self, url, body):
        if sys.version[0] == '2':
            return self._opener.open(url, body).read()
        else:
            return self._opener.open(url, body.encode()).read().decode('utf-8')

    def login(self):
        logging.debug('Login to %s', self._host)
        data = {'u': self._username, 'p': self._password, 'referer': '/'}
        response = self._session.post(
            "http://" + self._host + "/system/http/login", data=data)

        if response.status_code != 200:
            self._mess_id = None
            logging.error('Response content %s', response.content)
            raise SHC_Client_Exception('bad username or password')

        self._mess_id = 0

    def rpc(self, method, params=None):
        if self._mess_id is None:
            self.login()

        self._mess_id += 1

        payload = {"jsonrpc": "2.0", "method": method,
                   "params": params, "id": self._mess_id}

        response = self._session.post(
            "http://" + self._host + "/remote/json-rpc", json=payload)

        if response.status_code == 401:
            self.login()
            response = self._session.post(
                "http://" + self._host + "/remote/json-rpc", json=payload)

        if response.status_code == 200:
            return response.json()['result']

        raise xComfortApiException('RPC erron %s' % response.status_code)

    def get_system_info(self):
        return self.rpc("Settings/getSystemInfo")

    def is_user_advanced(self):
        return self.rpc("Settings/isUserAdvanced")['advanced']

    def get_zones(self):
        return self.rpc("HFM/getZones")

    def get_functions(self, zoneId):
        return self.rpc("HFM/getFunctions", zoneId)

    def get_macros(self, zoneId):
        return self.rpc("MacroFunction/getMacros", zoneId)

    def get_devices(self, zoneId):
        return self.rpc("StatusControlFunction/getDevices", [zoneId, ""])

    def get_dashboard(self, zoneId):
        "vraci poccet aktivnich zarizeni"
        return self.rpc("StatusControlFunction/getDashboard", zoneId)

    def control_device(self, zoneId, deviceId, operation):
        return self.rpc("StatusControlFunction/controlDevice", [zoneId, deviceId, str(operation)])
