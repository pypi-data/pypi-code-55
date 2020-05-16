import json
import traceback

import yaml

from definitions import DEBUG, LOG

from .enums import ContentType, Status
from .request import Request


class Response():

    def __init__(self, status:Status=Status.OK):
        self.response_body = None
        self.status = status
        self.headers = dict()
        self.set_content_type(ContentType.PLAIN)

    def body(self, response_body:str):
        self.response_body = response_body
        return self

    def html(self, html:str):
        self.set_content_type(ContentType.HTML)
        return self.body(json.dumps(html))

    def yaml(self, response:dict):
        self.set_content_type(ContentType.YAML)
        return self.body(yaml.dump(response))

    def json(self, response:dict):
        self.set_content_type(ContentType.JSON)
        return self.body(json.dumps(response))

    def get_status_code(self):
        return self.status.value[1]

    def set_content_type(self, content_type:ContentType):
        self.header('Content-Type', content_type.value)

    def header(self, header_name, header_value):
        self.headers[header_name] = header_value
        return self

    def not_found(self, request:Request):
        self.status = Status.NOT_FOUND
        return self.__set_response(request, 'Resource not found')

    def forbidden(self, request:Request):
        self.status = Status.FORBIDDEN
        return self.__set_response(request, 'Fobidden')

    def server_error(self, request:Request, exc_info=None):
        self.status = Status.SERVER_ERROR
        data = {}
        if exc_info:
            if DEBUG:
                data['exception'] = traceback.format_exception(*exc_info)
            else:
                LOG.error(self.status.value, exc_info=exc_info)
        return self.__set_response(request, 'Internal server error', data)

    def __set_response(self, request:Request, message, data:dict={}):
        if request.get_header('ACCEPT') == 'application/json':
            self.json({
                'status': self.status.value[0],
                'message': message,
                **data
            })
        else:
            self.body(message + "\n" + str(data) if data else message)
        return self
