# Copyright (c) 2013 Qumulo, Inc.
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

import qumulo.lib.request as request

@request.request
def get_node_state(conninfo, credentials):
    method = "GET"
    uri = "/v1/node/state"

    return request.rest_request(conninfo, credentials, method, uri)

