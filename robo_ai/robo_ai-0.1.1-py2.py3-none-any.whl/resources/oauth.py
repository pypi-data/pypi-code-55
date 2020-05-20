import requests
from requests.auth import HTTPBasicAuth

from robo_ai.exception.api_error import ApiError
from robo_ai.exception.invalid_credentials_error import InvalidCredentialsError
from robo_ai.exception.invalid_token_error import InvalidTokenError
from robo_ai.model.auth.access_info import AccessInfo
from robo_ai.model.auth.access_token import AccessToken
from robo_ai.resources.client_resource import ClientResource


class OauthResource(ClientResource):

    def authenticate(self, api_key: str) -> AccessToken:
        config = self.get_config()
        data = {
            'grant_type': 'client_credentials',
            'apiKey': api_key,
        }
        auth = HTTPBasicAuth(
            config.http_auth_username,
            config.http_auth_password
        )
        endpoint = config.base_endpoint + '/oauth/token'
        response = requests.post(endpoint, data=data, auth=auth)
        if response.status_code == requests.codes.ok:
            tokens = response.json()
            return AccessToken(
                tokens['access_token'],
                tokens['token_type'],
                tokens['expires_in'],
                tokens['scope']
            )
        elif response.status_code == 401:
            raise InvalidCredentialsError()
        else:
            raise ApiError()

    def get_token_info(self, token: str) -> AccessInfo:
        config = self.get_config()
        auth = HTTPBasicAuth(
            config.http_auth_username,
            config.http_auth_password
        )
        data = {
            'token': token,
        }
        endpoint = config.base_endpoint + '/oauth/check_token/'
        response = requests.post(endpoint, data=data, auth=auth)
        if response.status_code == requests.codes.ok:
            info_dict = response.json()
            return AccessInfo(
                info_dict['active'],
                info_dict['exp'],
                info_dict['authorities'],
                info_dict['client_id'],
                info_dict['scope'],
            )
        elif response.status_code == 401:
            raise InvalidTokenError()
        else:
            raise ApiError()
