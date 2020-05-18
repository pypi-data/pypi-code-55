import requests

from shield34_reporter.proxy import get_shield34_proxy


def request(method, url, **kwargs):
    return requests.request(method, url, proxies=get_shield34_proxy(), **kwargs)


def get(url, params=None, **kwargs):
    return requests.get(url, params, proxies=get_shield34_proxy(), **kwargs)


def options(url, **kwargs):
    return requests.options(url, proxies=get_shield34_proxy(), **kwargs)


def head(url, **kwargs):
    return requests.head(url, proxies=get_shield34_proxy(), **kwargs)


def post(url, data=None, json=None, **kwargs):
    return requests.post(url, data=data, json=json, proxies=get_shield34_proxy(), **kwargs)


def put(url, data=None, **kwargs):
    return requests.put(url, data=data, proxies=get_shield34_proxy(), **kwargs)


def patch(url, data=None, **kwargs):
    return requests.patch(url, data=data, proxies=get_shield34_proxy(), **kwargs)


def delete(url, **kwargs):
    return requests.delete(url, proxies=get_shield34_proxy(), **kwargs)
