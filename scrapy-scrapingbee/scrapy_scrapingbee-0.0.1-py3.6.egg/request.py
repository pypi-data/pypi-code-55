import base64
import copy
import urllib

from scrapy import Request


def process_url(value):
    return urllib.parse.quote(value)


def process_boolean(value):
    return 'true' if value is True else 'false'


def process_js_snippet(value):
    return base64.b64encode(value.encode()).decode()


def process_params(params):
    new_params = {}
    for k, v in params.items():
        if isinstance(k, bool):
            new_params[k] = process_boolean(v)
        elif k == 'js_snippet':
            new_params[k] = process_js_snippet(v)
        else:
            new_params[k] = v
    return new_params


class ScrapingBeeRequest(Request):
    
    def __init__(self, url, params=None, meta=None, **kwargs):
        if params is None:
            params = {}

        meta = copy.deepcopy(meta) or {}
        meta['scrapingbee'] = {
            'params': process_params(params)
        }
        meta['scrapingbee']['params']['url'] = process_url(url)

        super().__init__(url, meta=meta, **kwargs)
