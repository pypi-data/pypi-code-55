# coding=u8
import requests
from KE.exceptions import ResourceUnavailable
from KE.log import LoggingMixin


class Base(LoggingMixin):
    def __init__(self, client):
        self.id = None
        self._client = client
        self.debug = client.debug

    def __hash__(self):
        class_name = type(self).__name__
        return hash(class_name) ^ hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        raise NotImplementedError

    def __getstate__(self):
        # __getstate__ should return a dict of attributes that you want to pickle.
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        # __setstate__ should setup your object with the provided dict.
        self.__dict__.update(d)


class BaseClient(LoggingMixin):
    def __init__(self, debug=False):
        self.debug = debug

    def _to_curl(self,
                 uri,
                 method='GET',
                 headers=None,
                 params=None,
                 body=None,
                 files=None):
        """construct a curl command for test"""
        if headers is None:
            headers = self.headers
        if params is None:
            params = {}
        if body is None:
            body = {}

        # construct the full URL without query parameters
        if uri[0] == '/':
            uri = uri[1:]
        url = 'http://{host}:{port}/kylin/api/{uri}'.format(
            host=self.host, port=self.port, uri=uri
        )

        command = "curl -X {method} -H {headers} -d '{data}' '{url}'"
        data = body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
        headers = " -H ".join(headers)
        return command.format(method=method, headers=headers, data=data, url=url)

    def fetch_json(self,
                   uri,
                   method='GET',
                   headers=None,
                   params=None,
                   body=None,
                   files=None):
        """Fetch JSON"""
        if headers is None:
            headers = self.headers
        if params is None:
            params = {}
        if body is None:
            body = {}

        # construct the full URL without query parameters
        if uri[0] == '/':
            uri = uri[1:]
        url = 'http://{host}:{port}/kylin/api/{uri}'.format(
            host=self.host, port=self.port, uri=uri
        )
        self.logger.debug('headers: %s' % headers)
        self.logger.debug('url: %s' % url)
        self.logger.debug('params: %s' % params)
        self.logger.debug('body: %s' % body)
        response = requests.request(method, url,
                                    params=params,
                                    headers=headers,
                                    json=body,
                                    auth=(self.username, self.password))
        if response.status_code != 200:
            raise ResourceUnavailable("%s at %s" % (response.text, url), response)
        json_obj = response.json()

        return json_obj

    def __repr__(self):
        return "<KE {version} Host {host}>".format(version=self.version, host=self.host)
