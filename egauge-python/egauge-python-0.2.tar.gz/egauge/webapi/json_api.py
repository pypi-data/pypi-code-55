#
# Copyright (c) 2020 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
'''This module provides helper methods for accessing JSON web services.'''
import logging
import json

import requests

from .error import Error

log = logging.getLogger(__name__)

class JSONAPIError(Error):
    '''Raised if for any JSON API errors.'''

class UnauthenticatedError(Error):
    '''Raised when a request fails with HTTP status code 401.'''

def get(resource, **kwargs):
    '''Issue GET request for RESOURCE and return the parsed JSON data or
    None if the request failed or returned invalid JSON data.
    Additional keyword arguments are passed on to requests.get().

    '''
    try:
        r = requests.get(resource, **kwargs)
    except requests.exceptions.RequestException as e:
        raise JSONAPIError('requests.get exception.', e)
    if r.status_code == 401:
        raise UnauthenticatedError()
    if r.status_code < 200 or r.status_code > 299:
        log.exception('HTTP status code %s.  Keyword args: %s',
                      r.status_code, kwargs)
        raise JSONAPIError('Unexpected HTTP status code.', r.status_code)
    try:
        reply = r.json()
    except ValueError as e:
        raise JSONAPIError('Invalid JSON data.', e)
    return reply

def post(resource, json_data, **kwargs):
    '''Issue POST request for RESOURCE and return parsed JSON reply or
    None if the request failed or returned invalid JSON data.
    Additional keyword arguments are passed on to requests.post().

    '''
    headers = kwargs.get('headers', {})
    headers['Content-Type'] = 'application/json'
    kwargs['headers'] = headers
    try:
        r = requests.post(resource, data=json.dumps(json_data), **kwargs)
    except requests.exceptions.RequestException as e:
        raise JSONAPIError('requests.post exception.', e)
    if r.status_code == 401:
        raise UnauthenticatedError()
    if not 200 <= r.status_code <= 299:
        log.exception('HTTP status code %s.  Data: %s, keyword args: %s',
                      r.status_code, json_data, kwargs)
        raise JSONAPIError('Unexpected HTTP status code.', r.status_code)
    try:
        reply = r.json()
    except ValueError:
        raise JSONAPIError('Invalid JSON data.', e)
    return reply
