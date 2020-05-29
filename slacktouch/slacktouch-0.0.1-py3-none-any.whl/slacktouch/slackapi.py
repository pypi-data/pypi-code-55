import json
import os

class SlackHook():
    def __init__(self):
        self.default_command = '''curl -X POST -H 'Content-type: application/json' --data '{}' {}'''
        self.webhook_url = None

    def setWebHookUrl(self, webhook_url):
        self.webhook_url = webhook_url

    def sendMessage(self, message):
        self.message = {"text": "{}".format(message)}
        os.system(self.default_command.format(json.dumps(self.message), self.webhook_url))
