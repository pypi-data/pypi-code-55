# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import hashlib
import json

import arrow


class JDUBaseAPI(object):

    API_BASE_URL = None

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if self.API_BASE_URL:
            kwargs['api_base_url'] = self.API_BASE_URL
        return self._client.post(url, **kwargs)

class JDUOpenAPI(JDUBaseAPI):

    API_BASE_URL = 'https://router.jd.com/api'

    def __init__(self, client=None):
        super(JDUOpenAPI, self).__init__(client)

    def _get_url(self):
        return self.API_BASE_URL

    def _get(self, url, params=None, **kwargs):
        kwargs['params'] = params
        return super(JDUOpenAPI, self)._get(url, **kwargs)

    def get(self, api_method, params, **kwargs):
        _params = self.package(api_method, params)
        return self._get(self._get_url(), _params, **kwargs)

    def _get_access_token(self):
        return None

    def sign_params(self, params):
        params.pop('sign')
        params.pop('sign_method')
        app_secret = self._client.app_secret
        _sign_list = []
        for key in sorted(params.keys()):
            s = '%s%s' % (key, params[key])
            _sign_list.append(s)
        _sign = ''.join(_sign_list)
        _sign = '%s%s%s' % (app_secret, _sign, app_secret)
        _sign = hashlib.md5(_sign.encode("utf-8")).hexdigest().upper()
        return _sign

    def package(self, api_method, params):
        param_json = json.dumps(params)
        timestamp = arrow.utcnow().to('+08:00').format('YYYY-MM-DD HH:mm:ss')

        access_token = self._get_access_token()

        system_params = {
            'method': api_method,
            'app_key': self._client.app_key,
            'format': 'json',
            'v': self._client.version,
            'param_json': param_json,
            'timestamp': timestamp,
            'sign': '',
            'sign_method': 'md5'
        }

        if access_token:
            system_params['access_token'] = access_token

        sign = self.sign_params(system_params)
        system_params['sign'] = sign
        return system_params


class JDUWebAPI(JDUBaseAPI):

    API_BASE_URL = 'https://union.jd.com/api/'

    def __init__(self, client=None):
        super(JDUWebAPI, self).__init__(client)

    def get_header(self, ext_headers=None):
        _headers = {
            'accept': 'application/json, text/plain, */*',
            'authority': 'union.jd.com',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': self._client.get_cookie()
        }

        if isinstance(ext_headers, dict):
            _headers.update(ext_headers)

        return _headers

    def _get(self, url, params=None, ext_headers=None, **kwargs):
        kwargs['params'] = params
        kwargs['headers'] = self.get_header(ext_headers)
        return super(JDUWebAPI, self)._get(url, **kwargs)

    def _post(self, url, params=None, data=None, ext_headers=None, **kwargs):
        kwargs['params'] = params
        kwargs['data'] = data
        kwargs['headers'] = self.get_header(ext_headers)
        return super(JDUWebAPI, self)._get(url, **kwargs)

    def post(self, url, data=None, params=None, ext_headers=None, **kwargs):
        return self._post(url, params, data, ext_headers, **kwargs)