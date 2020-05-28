#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json


class HttpRequest:
    def __init__(self, url: str):
        self.url = url
        self.data = {}
        self.headers = {}

    def get(self):
        self.response = requests.get(self.url, headers=self.headers)
        return self

    def post(self):
        self.response = requests.post(self.url, data=self.data, headers=self.headers)
        return self

    def set_data(self, data: dict):
        self.data = data
        return self

    def set_headers(self, headers: dict):
        self.headers = headers
        return self

    def dumps_response(self):
        return json.dumps(json.loads(self.response.text), indent=2)
