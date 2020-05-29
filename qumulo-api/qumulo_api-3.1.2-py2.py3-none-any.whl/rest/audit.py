# Copyright (c) 2019 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# qumulo_python_versions = { 2, 3 }

from __future__ import absolute_import
from __future__ import unicode_literals

import warnings

import qumulo.lib.request as request

#                _
#  ___ _   _ ___| | ___   __ _
# / __| | | / __| |/ _ \ / _` |
# \__ \ |_| \__ \ | (_) | (_| |
# |___/\__, |___/_|\___/ \__, |
#      |___/             |___/
#  FIGLET: syslog
#


@request.request
def get_syslog_config(conninfo, credentials):
    method = 'GET'
    uri = '/v1/audit/syslog/config'
    return request.rest_request(conninfo, credentials, method, uri)


@request.request
def set_syslog_config(
    conninfo,
    credentials,
    enabled=None,
    server_address=None,
    server_port=None,
    etag=None,
):
    method = 'PATCH'
    uri = '/v1/audit/syslog/config'
    body = dict()
    if enabled is not None:
        body['enabled'] = enabled
    if server_address is not None:
        body['server_address'] = server_address
    if server_port is not None:
        body['server_port'] = server_port
    return request.rest_request(
        conninfo, credentials, method, uri, body=body, if_match=etag
    )


@request.request
def get_syslog_status(conninfo, credentials):
    method = 'GET'
    uri = '/v1/audit/syslog/status'
    return request.rest_request(conninfo, credentials, method, uri)


#       _                 _               _       _
#   ___| | ___  _   _  __| |_      ____ _| |_ ___| |__
#  / __| |/ _ \| | | |/ _` \ \ /\ / / _` | __/ __| '_ \
# | (__| | (_) | |_| | (_| |\ V  V / (_| | || (__| | | |
#  \___|_|\___/ \__,_|\__,_| \_/\_/ \__,_|\__\___|_| |_|
#  FIGLET: cloudwatch
#


@request.request
def get_cloudwatch_config(conninfo, credentials):
    method = 'GET'
    uri = '/v1/audit/cloudwatch/config'
    return request.rest_request(conninfo, credentials, method, uri)


@request.request
def set_cloudwatch_config(
    conninfo, credentials, enabled=None, log_group_name=None, region=None
):
    method = 'PATCH'
    uri = '/v1/audit/cloudwatch/config'
    body = dict()
    if enabled is not None:
        body['enabled'] = enabled
    if log_group_name is not None:
        body['log_group_name'] = log_group_name
    if region is not None:
        body['region'] = region
    return request.rest_request(conninfo, credentials, method, uri, body=body)


@request.request
def get_cloudwatch_status(conninfo, credentials):
    method = 'GET'
    uri = '/v1/audit/cloudwatch/status'
    return request.rest_request(conninfo, credentials, method, uri)


#      _                               _           _
#   __| | ___ _ __  _ __ ___  ___ __ _| |_ ___  __| |_
#  / _` |/ _ \ '_ \| '__/ _ \/ __/ _` | __/ _ \/ _` (_)
# | (_| |  __/ |_) | | |  __/ (_| (_| | ||  __/ (_| |_
#  \__,_|\___| .__/|_|  \___|\___\__,_|\__\___|\__,_(_)
#            |_|
#                                             __ _
#  _ __ ___ _ __ ___   _____   _____    __ _ / _| |_ ___ _ __
# | '__/ _ \ '_ ` _ \ / _ \ \ / / _ \  / _` | |_| __/ _ \ '__|
# | | |  __/ | | | | | (_) \ V /  __/ | (_| |  _| ||  __/ |
# |_|  \___|_| |_| |_|\___/ \_/ \___|  \__,_|_|  \__\___|_|
#  _____  _____  ___
# |___ / |___ / / _ \
#   |_ \   |_ \| | | |
#  ___) | ___) | |_| |
# |____(_)____(_)___/
#  FIGLET: deprecated: remove after 3.3.0
#

# The following functions are deprecated and will be removed after version
# 3.3.0. They have been renamed to include the word 'syslog' as seen earlier in
# this file.


@request.request
def get_config(conninfo, credentials):
    warnings.warn(
        'get_config is deprecated, use get_syslog_config instead', DeprecationWarning
    )
    return get_syslog_config(conninfo, credentials)


@request.request
def set_config(
    conninfo,
    credentials,
    enabled=None,
    server_address=None,
    server_port=None,
    etag=None,
):
    warnings.warn(
        'set_config is deprecated, use set_syslog_config instead', DeprecationWarning
    )
    return set_syslog_config(
        conninfo, credentials, enabled, server_address, server_port, etag
    )


@request.request
def get_status(conninfo, credentials):
    warnings.warn(
        'get_status is deprecated, use get_syslog_status instead', DeprecationWarning
    )
    return get_syslog_status(conninfo, credentials)
