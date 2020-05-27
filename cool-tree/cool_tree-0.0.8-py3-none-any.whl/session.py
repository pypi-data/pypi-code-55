import os
import configparser
import requests
import json
import copy
import base64

from spb.command import Command
from spb.models.project import Project


class Session:
    endpoint = "https://api.dev.superb-ai.com/graphql"
    headers = {
        'content-type': 'application/json',
        'cache-control': 'no-cache',
        'X-API-KEY': None,
        'Authorization': None
    }

    def __init__(self, profile=None, account_name=None, access_key=None):
        self.credential = None
        self._set_credential(
            profile=profile, account_name=account_name, access_key=access_key)

    def _set_credential(self, profile=None, account_name=None, access_key=None):
        if not profile and not account_name and not access_key:
            profile = 'default'

        if profile:
            credential_path = os.path.expanduser('~') + '/.spb/credentials'
            credential_path = credential_path.replace(os.sep, '/')
            # check exists credentials
            assert os.path.exists(credential_path), AssertionError(
                '** [ERROR] credentials file does not exists')
            config = self._read_config(credential_path=credential_path,
                                       profile=profile)  # get values from credential
            self.credential = config
        else:
            if account_name is None:
                raise AssertionError(
                    '** [ERROR] credential [account_name] does not exists')
            if access_key is None:
                raise AssertionError(
                    '** [ERROR] credential [access_key] does not exists')

            self.credential = {
                'account_name': account_name,
                'access_key': access_key
            }
        self.headers['X-API-KEY'] = self.credential['access_key']
        authorization_string = base64.b64encode(f'{self.credential["account_name"]}:{self.credential["access_key"]}'.encode("UTF-8"))
        self.headers['Authorization'] = f'Basic {authorization_string.decode("UTF-8")}'

    def _read_config(self, credential_path, profile):
        config = configparser.ConfigParser()
        config.read(credential_path)
        ret = {}
        vars = ['account_name', 'access_key']
        for var in vars:
            try:
                ret[var] = config.get(profile, var)
            except (configparser.NoSectionError, configparser.NoOptionError):
                raise AssertionError(
                    '** [ERROR] credential - key [{0}] does not exists'.format(var))
        return ret

    def execute(self, model, query):
        data = {
            'query': query,
            'variables': {}
        }
        data = json.dumps(data)
        try:
            response = requests.request(
                "POST", self.endpoint, data=data, headers=self.headers)
        except requests.exceptions.Timeout:
            raise Exception('Occurred Time out of this request')
        except requests.exceptions.RequestException:
            raise Exception('Network Error')
        except Exception:
            raise Exception('Unknown Error on requests')

        try:
            response = response.json()
        except:
            raise Exception(
                "Failed to parse response as JSON: %s", response.text)

        errors = response.get('errors', [])
        # TODO: Error Handling from Server

        res_data = response.get('data')
        return self._make_model_from_res(data=res_data, model=model)

    def _make_model_from_res(self, data, model):
        if data is None:
            return None
        data_keys = data.keys()
        json_datas = None
        for key in data_keys:
            if key.find(model.RESOURCE_NAME) != -1:
                json_datas = data[key]
        if isinstance(json_datas, list):
            result = []
            for json in json_datas:
                temp = self._json_to_model(model=model, args=json)
                result.append(temp)
            return result
        else:
            return self._json_to_model(model=model, args=json_datas)

    def _json_to_model(self, model, args):
        return model.res_to_model(args)
