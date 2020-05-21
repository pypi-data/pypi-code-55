# coding: utf-8
from requests.auth import HTTPBasicAuth
from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class VindiClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://sandbox-app.vindi.com.br/api/v1/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(VindiClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params["auth"] = HTTPBasicAuth(api_params.get("api_key"), "")

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass

    def get_api_root(self, api_params, **kwargs):
        if api_params.get('sandbox'):
            return 'https://sandbox-app.vindi.com.br/api/v1/'
        return 'https://app.vindi.com.br/api/v1/'


Vindi = generate_wrapper_from_adapter(VindiClientAdapter)
