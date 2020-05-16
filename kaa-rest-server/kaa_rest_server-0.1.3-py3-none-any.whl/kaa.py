import importlib
import sys

import kaa
from definitions import ENABLE_CORS

from .enums import Status
from .exceptions import KaaError, ResourceNotFoundError
from .filters import RequestFilter, ResponseFilter
from .openapi import OpenApi
from .request import Request
from .resources import Resources
from .response import Response


class Kaa():

    def __init__(self, env, start_response):
        self.start_response = start_response
        self.request = Request(env)
        self.resources = {}
        self.request_filters = {}
        self.response_filters = {}

    def register_resources(self, module:str, class_name:str):
        self.__register(self.resources, module, class_name)

    def register_filter_request(self, module:str, class_name):
        self.__register(self.request_filters, module, class_name)

    def register_filter_response(self, module:str, class_name):
        self.__register(self.response_filters, module, class_name)

    def __register(self, element, module, class_name):
        if module not in element:
            element[module] = []
        element[module].append(class_name)

    def serve(self):
        try:
            if self.request.method == 'OPTIONS':
                return self.__act_method_options()

            if self.request.path == '/openapi':
                return self.__get_openapi()

            self.__request_filters()
            for module_name in self.resources:
                for class_name in self.resources[module_name]:
                    response:Response = self.__run_resource(module_name, class_name)
                    if response:
                        self.__response_filters(response)
                        return self.__print_response(response)
            raise ResourceNotFoundError()
        except KaaError as e:
            return self.__print_response(e.response())
        except Exception:
            return self.__print_response(Response().server_error(self.request, sys.exc_info()))

    def __get_openapi(self):
        openapi = OpenApi().generate(self)
        response = Response()
        if self.request.get_header('ACCEPT') == 'application/json':
            response.json(openapi)
        else:
            response.yaml(openapi)
        return self.__print_response(response)

    def __act_method_options(self):
        if ENABLE_CORS:
            response = Response(Status.ACCEPTED)
            self.__response_filters(response)
        else:
            response = Response(Status.METHOD_NOT_ALLOWED)
        return self.__print_response(response.body(''))

    def __request_filters(self):
        def func(instance:RequestFilter):
            method_ = getattr(instance, 'filter')
            method_(instance, self.request)
        self.__call_filters(self.request_filters, func)

    def __response_filters(self, response:Response):
        def func(instance:ResponseFilter):
            method_ = getattr(instance, 'filter')
            method_(instance, self.request, response)
        self.__call_filters(self.response_filters, func)

    def __call_filters(self, filters, func):
        for module_name in filters:
            for class_name in filters[module_name]:
                func(self.__get_class(module_name, class_name))

    def __run_resource(self, module_name, class_name) -> Response:
        class_ = self.__get_class(module_name, class_name)
        instance:Resources = class_(self.request)
        for method_name in dir(class_):
            count = 1 + len(class_name) + 2
            if method_name[:2] == "__" or method_name[:count] == "_{}__".format(class_name):
                continue
            method_ = getattr(class_, method_name)
            result = method_(instance)
            if result:
                return result

    def __get_class(self, module_name, class_name):
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def __print_response(self, response:Response):
        headers = [(k, response.headers[k]) for k in response.headers]
        headers.append(('Server', '{}/{}'.format(kaa.NAME, kaa.VERSION)))
        self.start_response(response.get_status_code(), headers)
        return [response.response_body.encode("utf8")]
