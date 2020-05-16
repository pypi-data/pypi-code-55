from .authorization import Authorization
from .decorators import AUTH, GET, PATH, POST, PUT, DELETE
from .enums import ContentType, Status
from .exceptions import *
from .filters import RequestFilter, ResponseFilter
from .kaa import Kaa
from .request import Request
from .resources import Resources
from .response import Response

NAME = 'KAA'
VERSION = '0.1'


class KaaServer:

    def get_kaa(self, env, start_response):
        pass

    def serve(self, env, start_response):
        return self.get_kaa(env, start_response).serve()

    def generate_openapi(self):
        pass
