import json
import requests

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "POST"


class Pipedrive(object):
    GET = GET
    POST = POST
    PUT = PUT
    DELETE = POST

    def __init__(self, token):
        self._token = token
        self._origin = "https://app.pipedrive.com"

    def request(self, method, path, data={}):
        r = requests.request(
            method,
            self._origin + path + "?api_token=%s" % self._token,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return r.json()
