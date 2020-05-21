# -*- coding: utf-8 -*-
import requests
import json
import os

class CustomersMailCloud:
    def __init__(self, api_user, api_key):
        if (api_user is None or api_user == ''):
            raise Exception('API User is required.')
        if (api_key is None or api_key == ''):
            raise Exception('API Key is required.')
        self.endpoints = {
            "trial": "https://sandbox.smtps.jp/api/v2/emails/send.json",
            "standard": "https://te.smtps.jp/api/v2/emails/send.json",
            "pro": "https://SUBDOMAIN.smtps.jp/api/v2/emails/send.json"
        }
        self.api_user = api_user
        self.api_key = api_key
        self.url = ""
        self.to_address = []
        self.from_address = {}
        self.subject = ''
        self.text = ''
        self.html = ''
        self.attachments = []

    def trial(self):
        self.url = self.endpoints['trial']
    def standard(self):
        self.url = self.endpoints['standard']
    def pro(self, subdomain):
        if (subdomain is None or subdomain == ''):
            raise Exception('サブドメインは必須です')
        self.url = self.endpoints['pro'].replace('SUBDOMAIN', subdomain)
    def addTo(self, name, address):
        self.to_address.append({
            'name': name,
            'address': address
        })
    def setFrom(self, name, address):
        self.from_address = {
            'name': name,
            'address': address
        }
    def addFile(self, file):
        self.attachments.append(file)
    def send(self):
        if (self.url == ''):
             raise Exception('契約プランを選択してください（trial/standard/pro）')
        if (self.from_address['address'] is None or self.from_address['address'] == ''):
            raise Exception('送信元アドレスは必須です')
        if (len(self.to_address) == 0):
            raise Exception('送り先が指定されていません')
        if (self.subject is None or self.subject == ''):
            raise Exception('件名は必須です')
        if (self.text is None or self.text == ''):
            raise Exception('メール本文は必須です')
        
        params = { 
          'api_user': self.api_user,
          'api_key': self.api_key,
          'to': self.to_address,
          'from': self.from_address,
          'subject': self.subject,
          'text': self.text
        }
        
        if (self.html != ''):
            params.html = self.html
        if len(self.attachments) > 0:
            params["attachments"] = len(self.attachments)
            files = {}
            for key in params:
                if type(params[key]) is not str:
                    params[key] = json.dumps(params[key])
            for i, attachment in enumerate(self.attachments):
                file = open(attachment, 'rb')
                files[f"attachment{str(i + 1)}"] = (os.path.basename(attachment), file)
            res = requests.post(self.url, data=params, files=files)
        else:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            res = requests.post(self.url, json=params, headers=headers)
        if res.status_code == 200:
            return json.loads(res.content)
        else:
            raise Exception(res.content)
