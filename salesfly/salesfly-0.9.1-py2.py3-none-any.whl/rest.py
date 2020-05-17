import requests
import logging
import json
import string

# try:
#    from urllib import quote
# except ImportError:
#    from urllib.parse import quote

from salesfly.errors import APIConnectionError, APITimeoutError, ResponseError
from salesfly.version import VERSION

BOUNDARY_CHARS = string.digits + string.ascii_letters
USER_AGENT = "salesfly-python/{0}".format(VERSION)


class RestClient:
    def __init__(self, api_key=None, api_base_url=None, timeout=None):
        """
        @param kwargs: Optional parameters
        """
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.timeout = timeout

    def get(self, path, headers={}):
        """
        Execute a HTTP GET
        """
        return self.execute("GET", path, headers=headers)

    def post(self, path, data, headers={}):
        """
        Execute a HTTP POST
        """
        return self.execute("POST", path, data, headers)

    def patch(self, path, data, headers={}):
        """
        Execute a HTTP PATCH
        """
        return self.execute("PATCH", path, data, headers)

    def put(self, path, data, headers={}):
        """
        Execute a HTTP PUT
        """
        return self.execute("PUT", path, data, headers)

    def delete(self, path, headers={}):
        """
        Execute a HTTP DELETE
        """
        return self.execute("DELETE", path, headers=headers)

    def execute(self, method, path, data=None, headers={}):
        """
        Execute a HTTP request
        """
        logging.debug("Sending HTTP request")
        # logging.debug("{0} {1}".format(method, path))

        url = self.api_base_url + path  # quote(path, safe=',')

        allHeaders = {
            "Authorization": "Bearer {0}".format(self.api_key),
            "Accept": "application/json",
            "User-Agent": USER_AGENT
        }
        allHeaders.update(headers)

        try:
            params = {}
            if method == "GET":
                if data is not None:
                    params.update(data)
            elif method in ["POST", "PUT", "PATCH"]:
                if isinstance(data, dict):
                    data = json.dumps(data)
            resp = requests.request(
                method, url, headers=allHeaders, params=params, data=data, timeout=self.timeout)
        except requests.exceptions.Timeout as e:
            raise APITimeoutError("Request timed out: " + repr(e))
        except requests.exceptions.RequestException as e:
            raise APIConnectionError("Unable to connect to server: " + repr(e))

        if resp.status_code not in [200, 201]:
            try:
                content = resp.json()
                message = content["message"]
                code = content["code"]
            except (KeyError, ValueError):
                # Not JSON response, or message set
                if resp.status_code == 501:
                    message = "Not implemented"
                elif resp.status_code == 502:
                    message = "Bad gateway"
                elif resp.status_code == 503:
                    message = "Service unavailable"
                elif resp.status_code == 504:
                    message = "Gateway timeout"
                else:
                    message = "Internal server error"
            raise ResponseError(resp.status_code, msg=message, code=code)

        # Parse JSON, return data only
        if resp.headers["Content-Type"] == "application/pdf":
            return resp.content
        result = json.loads(resp.content)
        return result["data"]
