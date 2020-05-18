import json
import requests
from urllib.parse import urlencode

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
        url = self._origin + path + "?api_token=%s" % self._token
        if method == GET and data:
            if data:
                url += "&" + urlencode(data)
        r = requests.request(
            method,
            url,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return r.json()

    def __getattr__(self, name):
        def wrapper(data={}):
            action, raw_path = name.split("_", 1)
            method = {"get": GET, "create": POST, "update": PUT, "delete": DELETE}[
                action
            ]
            path = raw_path.replace("_", "/")
            if method == PUT:
                id = data.pop("id")
                path = "%s/%d" % (path, id)
            r_data = self.request(method, "/v1/" + path, data)
            if "error" in r_data:
                raise self.Error(r_data)
            return r_data

        return wrapper

    class Error(Exception):
        def __init__(self, response):
            self.response = response

        def __str__(self):
            return self.response.get("error", "No error provided")
