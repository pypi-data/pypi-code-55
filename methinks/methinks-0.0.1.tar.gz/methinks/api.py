import os
import json
import requests

from methinks.db import Entry
from methinks.utils import data_to_json


class MethinksAPI(object):
    """Class that implements api to manipulate remote"""

    STATUS = 'status'
    MESSAGE = 'message'

    def __init__(self, url):
        super().__init__()
        self.url = url.rstrip('/')
        # Make sure we are using https
        # assert('https' in self.url)
        self.status = None
        self.message = None

    def _post_json(self, url, data_dict):
        SECRET_TOKEN = os.environ['METHINKS_TOKEN']
        data_dict['token'] = SECRET_TOKEN
        data = data_to_json(data_dict)
        r = requests.post(url,
                          data=data,
                          headers={'Content-Type': 'application/json'})
        response = json.loads(r.text)
        self.status = response.get(MethinksAPI.STATUS)
        self.message = response.get(MethinksAPI.MESSAGE)
        return response

    def _get_json(self, url):
        SECRET_TOKEN = os.environ['METHINKS_TOKEN']
        params = dict(token=SECRET_TOKEN)
        response = json.loads(requests.get(url, params=params).text)
        self.status = response.pop(MethinksAPI.STATUS)
        self.message = response.pop(MethinksAPI.MESSAGE)
        return response

    def check_status(self):
        attempt = requests.get(self.url)
        if attempt.status_code != 200:
            raise ValueError('Nothing running at: %s' % self.url)

    def get_latest(self):
        r = self._get_json('%s/entries/latest' % self.url)
        if self.status:
            entry = Entry.from_dict(r['data'])
        else:
            entry = None
        return entry

    def create_entry(self, entry):
        d_dict = dict(text=entry.text,
                      date=entry.date,
                      **entry.misc)
        r = self._post_json('%s/entries/create' % self.url, d_dict)
        if self.status:
            entry = Entry.from_dict(r['data'])
        else:
            entry = None
        return entry

    def update_entry(self, entry):
        d_dict = dict(text=entry.text,
                      date=entry.date,
                      **entry.misc)
        r = self._post_json('%s/entries/update' % self.url, d_dict)
        if self.status:
            entry = Entry.from_dict(r['data'])
        else:
            entry = None
        return entry

    def delete_entry(self, entry):
        d_dict = dict(date=entry.date)
        self._post_json('%s/entries/delete' % self.url, d_dict)
        return self.status
