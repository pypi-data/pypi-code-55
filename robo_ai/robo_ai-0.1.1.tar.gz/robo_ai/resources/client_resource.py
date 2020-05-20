from enum import Enum
from typing import Optional, BinaryIO, Type, Union, Callable
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

import cattr
import requests

from robo_ai.exception.api_error import ApiError
from robo_ai.exception.invalid_credentials_error import InvalidCredentialsError
from robo_ai.exception.not_authorized_error import NotAuthorizedError
from robo_ai.exception.not_found_error import NotFoundError
from robo_ai.model.base_response import BaseResponse
from robo_ai.model.config import Config
from robo_ai.model.session import Session


class RequestMethod(Enum):
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    DELETE = 'delete'


class ClientResource(object):
    __config: Config = None
    __session: Session = None
    __resources: dict = {}

    def __init__(self, config: Config, session: Session):
        self.__config = config
        self.__session = session
        self._register_resources()

    def get_config(self) -> Config:
        return self.__config

    def get_auth_headers(self) -> dict:
        token = self.get_access_token()
        return {
            'Authorization': 'bearer %s' % token,
        } if token else {}

    def get_access_token(self) -> Optional[str]:
        if self.__session:
            return self.__session.access_token
        return None

    def execute_request(self, method: RequestMethod, url: str, response_class: Type[BaseResponse] = None,
                        json_data: dict = None, data: Union[dict, BinaryIO] = None, files: dict = None,
                        params: dict = None, headers: dict = {}, auth_headers=True,
                        progress_callback: Callable[[MultipartEncoderMonitor], None] = None):

        config = self.get_config()
        full_url = config.base_endpoint + url

        if auth_headers:
            auth_headers = self.get_auth_headers()
            headers = {
                **headers,
                **auth_headers
            }

        data_fields = None
        if data:
            data_fields = MultipartEncoder(fields=data)
            headers['Content-Type'] = data_fields.content_type
            if progress_callback:
                data_fields = MultipartEncoderMonitor(data_fields, progress_callback)

        response = requests.request(method.value, full_url, headers=headers, params=params, data=data_fields,
                                    json=json_data, files=files)

        # all 2xx codes are considered success
        is_success = response.status_code // 100 == 2

        if is_success:
            if response_class:
                assistant = cattr.structure(response.json(), response_class)
                return assistant
            else:
                return response.content
        elif response.status_code == 401:
            raise InvalidCredentialsError()
        elif response.status_code == 403:
            raise NotAuthorizedError()
        elif response.status_code == 404:
            raise NotFoundError()
        else:
            raise ApiError()

    def _add_resource(self, name: str, resource_type: Type['ClientResource']):
        self.__resources[name] = resource_type(self.__config, self.__session)

    def _get_resource(self, name: str):
        return self.__resources[name]

    def _register_resources(self):
        pass
