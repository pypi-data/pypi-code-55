#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json

from .decorator import waitingdots

from taz.http import HttpRequest


@waitingdots
def test_010_get_method():
    req = HttpRequest("https://postman-echo.com/get?foo1=bar1&foo2=bar2")
    req.get()
    print(req.response.status_code)
    print(req.dumps_response())
    assert req.response.status_code == 200


@waitingdots
def test_020_post_method():
    req = HttpRequest("https://postman-echo.com/post")
    req.set_data({"foo1": "bar1"})
    req.post()
    print(req.response.status_code)
    print(req.dumps_response())
    assert req.response.status_code == 200
