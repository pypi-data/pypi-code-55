#  BSD 3-Clause License
#
#  Copyright (c) 2012, the Sentry Team, see AUTHORS for more details
#  Copyright (c) 2019, Elasticsearch BV
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE


import re

from hoss_agent.conf.constants import ERROR, MASK, SPAN, TRANSACTION, EVENT, ENCODED_MASK
from hoss_agent.utils import compat, varmap
from hoss_agent.utils.encoding import force_text
import base64
import json

SANITIZE_FIELD_NAMES = frozenset(
    ["authorization", "password", "secret", "passwd", "password", "token", "api_key", "access_token", "sessionid"]
)

SANITIZE_VALUE_PATTERNS = [re.compile(r"^[- \d]{16,19}$")]  # credit card numbers, with or without spacers


def for_events(*events):
    """
    :param events: list of event types

    Only calls wrapped function if given event_type is in list of events
    """
    events = set(events)

    def wrap(func):
        func.event_types = events
        return func

    return wrap


def remove_body(client, api_config, event):
    """
    Removes request.body from context

    :param client: an hoss_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    if event is not None:
        body_capture = api_config[
            "body_capture"] if api_config is not None else client.client.config.account_api_configuration.get(
            'body_capture')
        if body_capture == "Off":
            event["request"]['body'] = ENCODED_MASK
            event["response"]['body'] = ENCODED_MASK
        # todo handle onError
    return event


def sanitize_http_request_cookies(client, api_config, event):
    """
    Sanitizes http request cookies

    :param client: an hoss_agent client
    :param event: a transaction or error event
    :return: The modified event
    """

    # sanitize request.cookies dict
    try:
        cookies = event["request"]["cookies"]
        event["request"]["cookies"] = varmap(_sanitize, cookies)
    except (KeyError, TypeError):
        pass

    # sanitize request.header.cookie string
    try:
        cookie_string = event["request"]["headers"]["cookie"]
        event["request"]["headers"]["cookie"] = _sanitize_string(cookie_string, "; ", "=")
    except (KeyError, TypeError):
        pass
    return event


def sanitize_http_response_cookies(client, api_config, event):
    """
    Sanitizes the set-cookie header of the response
    :param client: an hoss_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        cookie_string = event["response"]["headers"]["set-cookie"]
        event["response"]["headers"]["set-cookie"] = _sanitize_string(cookie_string, ";", "=")
    except (KeyError, TypeError):
        pass
    return event


def sanitize_http_headers(client, api_config, event):
    """
    Sanitizes http request/response headers

    :param client: an hoss_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    # request headers
    headers_to_sanitize = []
    try:
        headers_to_sanitize = api_config[
            "sanitized_headers"] if api_config is not None else client.client.config.account_api_configurations.get(
            'sanitized_headers')
    except:
        pass

    try:
        headers = event["request"]["headers"]
        event["request"]["headers"] = varmap(lambda k, v: _sanitize(k, v, headers_to_sanitize), headers)
    except (KeyError, TypeError):
        pass

    # response headers
    try:
        headers = event["response"]["headers"]
        event["response"]["headers"] = varmap(lambda k, v: _sanitize(k, v, headers_to_sanitize), headers)
    except (KeyError, TypeError):
        pass

    return event


def sanitize_http_request_querystring(client, api_config, event):
    """
    Sanitizes http request query string

    :param client: an hoss_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        url = force_text(event["request"]["url"], errors="replace")
    except (KeyError, TypeError):
        return event

    parsed_url = compat.urlparse.urlparse(url)
    query = parsed_url.query
    if "=" in query:
        params_to_sanitize = []
        try:
            params_to_sanitize = api_config[
                "sanitized_query_params"] if api_config is not None else client.client.config.account_api_configurations.get(
                'sanitized_query_params')
        except:
            pass

        sanitized_query_string = _sanitize_string(query, "&", "=", params_to_sanitize)
        event["request"]["url"] = url.replace(query, sanitized_query_string)
    return event


def _do_sanitize_http_body(body, fields):
    if fields and body:
        json_path_fields = map(lambda f: f['value'], filter(lambda f: f['type'] == 'JSONPath', fields))
        try:
            decoded_body = json.loads(base64.b64decode(body))
            return base64.b64encode(json.dumps(varmap(lambda k, v: _sanitize(k, v, json_path_fields), decoded_body)).encode('utf-8'))
        except Exception as e:
            pass
    return body


def sanitize_http_body(client, api_config, event):
    """
    Sanitizes http request body. This only works if the request body
    is a query-encoded string. Other types (e.g. JSON) are not handled by
    this sanitizer.

    :param client: an hoss_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        body = force_text(event["request"]["body"], errors="replace")
    except (KeyError, TypeError):
        return event
    fields_to_sanitize = []
    try:
        fields_to_sanitize = api_config[
            "sanitized_body_fields"] if api_config is not None else client.client.config.account_api_configurations.get(
            'sanitized_body_fields')
    except:
        pass
    event["request"]["body"] = _do_sanitize_http_body(event["request"]["body"], fields_to_sanitize)
    event["response"]["body"] = _do_sanitize_http_body(event["response"]["body"], fields_to_sanitize)
    return event


def _sanitize(key, value, fields=SANITIZE_FIELD_NAMES):
    if value is None:
        return

    if isinstance(value, compat.string_types) and any(pattern.match(value) for pattern in SANITIZE_VALUE_PATTERNS):
        return MASK

    if isinstance(value, dict):
        # varmap will call _sanitize on each k:v pair of the dict, so we don't
        # have to do anything with dicts here
        return value

    if not key:  # key can be a NoneType
        return value

    key = key.lower()
    for field in fields:
        if field.lower() in key:
            # store mask as a fixed length for security
            return MASK
    return value


def _sanitize_string(unsanitized, itemsep, kvsep, fields=SANITIZE_FIELD_NAMES):
    """
    sanitizes a string that contains multiple key/value items
    :param unsanitized: the unsanitized string
    :param itemsep: string that separates items
    :param kvsep: string that separates key from value
    :return: a sanitized string
    """
    sanitized = []
    kvs = unsanitized.split(itemsep)
    for kv in kvs:
        kv = kv.split(kvsep)
        if len(kv) == 2:
            sanitized.append((kv[0], _sanitize(kv[0], kv[1], fields)))
        else:
            sanitized.append(kv)
    return itemsep.join(kvsep.join(kv) for kv in sanitized)
