# -*- coding: utf-8 -*-

import re
import time
import logging
import traceback
from itertools import chain
from urllib.parse import urljoin
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

import requests

from monapy import Binder
from monapy import Step
from bs4 import BeautifulSoup as bs


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
fmt = logging.Formatter('%(name)s:line %(lineno)s:%(asctime)s:\n%(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)


RequestInfo = namedtuple('RequestInfo', [
        'url',
        'method',
        'kwargs'
    ]
)


Selected = namedtuple('Selected', [
        'url',
        'selector',
        'request',
        'value'
    ]
)


class FLoad(Step):
    def __init__(self, method='GET', delay=0, **kwargs):
        self._method = method
        self._delay = delay
        self._kwargs = kwargs
        self._executor = ThreadPoolExecutor()

        self._filter_func = lambda info: True
        self._on_err_func = (
            lambda err, info:
                logger.error(
                    '%s\n%s' % (
                        info.url,
                        traceback.format_exc()
                    )
                )
        )

    def __del__(self):
        self._executor.shutdown()

    def filter(self, func):
        self._filter_func = func
        return self

    def on_error(self, func):
        self._on_err_func = func
        return self

    def make_all(self, iterable, **kwargs):
        return chain.from_iterable(
            self._executor.map(
                lambda val: self.make(val, **kwargs),
                iterable
            )
        )

    def make(self, req_addr, **kwargs):
        if hasattr(req_addr, 'url') and hasattr(req_addr, 'value'):
            base_url = req_addr.url
            url_ = req_addr.value
        elif isinstance(req_addr, str):
            base_url = ''
            url_ = req_addr
        elif isinstance(req_addr, bytes):
            base_url = ''
            url_ = req_addr.decode()
        else:
            logger.error(
                'FLoad.make(%s) must be Selected, str or bytes' % 
                type(req_addr)
            )
            return iter([])

        if not (
                url_.startswith('http://') or
                url_.startswith('https://') or
                url_.startswith('file://')
            ):
            url = urljoin(base_url, url_)
        else:
            url = url_

        kw = kwargs.copy()
        kw.update(self._kwargs)
        kw.update(stream=True)
        time.sleep(self._delay)

        try:
            resp = requests.request(self._method, url, **kw)
            if not self._filter_func(resp):
                return iter([])
        except Exception as err:
            kw.update(delay=self._delay)
            self._on_err_func(
                err,
                RequestInfo(url=url, method=self._method, kwargs=kw)
            )
            return iter([])

        return iter([resp])


# class FScan(Step):
#     def __init__(self, selector='', *, parser='html.parser'):
#         self._selector = selector.strip()
#         self._parser = parser
#         self._func = Binder()
#         self._request = []
#         self._executor = ThreadPoolExecutor()

#     def __del__(self):
#         self._executor.shutdown()

#     def map(self, func):
#         self._request.append(
#             'map',
#             getattr(func, 'name', repr(func))
#         )
#         self._func >> map << func
#         return self

#     def filter(self, func):
#         self._request.append(
#             (
#                 'filter',
#                 getattr(func, 'name', repr(func))
#             )
#         )
#         self._func >> filter << func
#         return self

#     def text(self):
#         self._request.append('text')
#         self._func >> map << (lambda e: e.text)
#         return self

#     def attr(self, attr_name):
#         sentinel = object()
#         self._request.append(('attr', attr_name))
#         (
#             self._func
#             >> map << (lambda e: e.get(attr_name, sentinel))
#             >> filter << (lambda e: e is not sentinel)
#         )
#         return self

#     def re(self, pattern, flags=0):
#         self._request.append(
#             (
#                 're',
#                 pattern,
#                 flags
#             )
#         )
#         self._func >> map << (lambda e: re.findall(pattern, str(e), flags))
#         return self

#     def make_all(self, iterable, **kwargs):
#         return chain.from_iterable(
#             self._executor.map(
#                 lambda val: self.make(val, **kwargs),
#                 iterable
#             )
#         )

#     def make(self, resp_cont, **kwargs):
#         if isinstance(resp_cont, requests.Response):
#             url = resp_cont.url
#             html_tree = bs(
#                 resp_cont.content,
#                 kwargs.get('parser', self._parser)
#             )
#         else:
#             url = ''
#             html_tree = bs(
#                 resp_cont,
#                 kwargs.get('parser', self._parser)
#             )

#         if self._selector:
#             tree_list = html_tree.select(self._selector)
#         else:
#             tree_list = [html_tree]

#         for res in self._func(tree_list):
#             yield Selected(
#                 url=url,
#                 selector=self._selector,
#                 request=self._request,
#                 value=res
#             )


class FScan(Step):
    def __init__(self, selector='', *, parser='html.parser'):
        self._selector = selector.strip()
        self._parser = parser
        self._func = Binder()
        self._request = []
        self._executor = ThreadPoolExecutor()
        self._on_err_func = (
            lambda err, cont:
                logger.error(
                    '%s\n' % traceback.format_exc()
                )
        )
        self._once = False
        self._in_all = False

    def __del__(self):
        self._executor.shutdown()

    def on_error(self, func):
        self._on_err_func = func
        return self

    def once(self):
        if 'once' not in self._request:
            self._request.append('once')
        self._once = True
        return self

    def all_in_one(self):
        if 'all_in_one' not in self._request:
            self._request.append('all_in_one')
        self._in_all = True
        return self

    def map(self, func):
        self._request.append(
            'map',
            getattr(func, 'name', repr(func))
        )
        self._func >> map << func
        return self

    def filter(self, func):
        self._request.append(
            (
                'filter',
                getattr(func, 'name', repr(func))
            )
        )
        self._func >> filter << func
        return self

    def text(self):
        self._request.append('text')
        self._func >> map << (lambda e: e.text)
        return self

    def attr(self, attr_name):
        sentinel = object()
        self._request.append(('attr', attr_name))
        (
            self._func
            >> map << (lambda e: e.get(attr_name, sentinel))
            >> filter << (lambda e: e is not sentinel)
        )
        return self

    def re(self, pattern, flags=0):
        self._request.append(
            (
                're',
                pattern,
                flags
            )
        )
        self._func >> map << (lambda e: re.findall(pattern, str(e), flags))
        return self

    def make_all(self, iterable, **kwargs):
        return chain.from_iterable(
            self._executor.map(
                lambda val: self.make(val, **kwargs),
                iterable
            )
        )

    def make(self, resp_cont, **kwargs):
        try:
            if isinstance(resp_cont, requests.Response):
                url = resp_cont.url
                html_tree = bs(
                    resp_cont.content,
                    kwargs.get('parser', self._parser)
                )
            else:
                url = ''
                html_tree = bs(
                    resp_cont,
                    kwargs.get('parser', self._parser)
                )
        except Exception as e:
            self._on_err_func(e, resp_cont)
            return

        if self._selector:
            tree_list = html_tree.select(self._selector)
        else:
            tree_list = [html_tree]

        if self._once:
            if len(tree_list) <= 0:
                return
            tree_list = [tree_list[0]]

        if self._in_all:
            yield Selected(
                    url=url,
                    selector=self._selector,
                    request=self._request,
                    value=tuple(self._func(tree_list))
                )
        else:
            for res in self._func(tree_list):
                yield Selected(
                    url=url,
                    selector=self._selector,
                    request=self._request,
                    value=res
                )

