from .version import __version__
from . import generic

import json
import os

class rasa(generic.generic):
    def __init__(self, apiKey,debug=False, printErrors=False, proxies=None):
        if 'DASHBOT_SERVER_ROOT' in os.environ:
            serverRoot = os.environ['DASHBOT_SERVER_ROOT']
        else:
            serverRoot = 'https://tracker.dashbot.io'
        self.urlRoot = serverRoot + '/track'
        self.apiKey = apiKey
        self.debug = debug
        self.printErrors = printErrors
        self.platform = 'rasa'
        self.version = __version__
        self.source = 'pip'
        self.proxies = proxies

    def logIncoming(self, data):
        url = self.urlRoot + '?apiKey=' + self.apiKey + '&type=incoming&platform=' + self.platform + '&v=' + self.version + '-' + self.source

        if self.debug:
            print('Dashbot Incoming:' + url)
            print(json.dumps(data))

        self.makeRequest(url, 'POST', data, proxies=self.proxies)

    def logOutgoing(self, data):
        url = self.urlRoot + '?apiKey=' + self.apiKey + '&type=outgoing&platform=' + self.platform + '&v=' + self.version + '-' + self.source

        if self.debug:
            print('Dashbot Outgoing:' + url)
            print(json.dumps(data))

        self.makeRequest(url, 'POST', data, proxies=self.proxies)

    @classmethod
    def from_endpoint_config(
        cls, broker_config
    ):
        if broker_config is None:
            return None
        return cls(**broker_config.kwargs)

    def publish(self, event):
        if event['event'] == 'user':
            self.logIncoming(event)
        elif event['event'] == 'bot':
            self.logOutgoing(event)
        elif event['event'] == 'action':
            if event['name'] != 'action_listen':
                self.logOutgoing(event)
