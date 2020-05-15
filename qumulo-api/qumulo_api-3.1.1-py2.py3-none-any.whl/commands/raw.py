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

from __future__ import absolute_import, unicode_literals

import json
import sys

import qumulo.lib.opts
import qumulo.lib.request as request

class RawCommand(qumulo.lib.opts.Subcommand):
    NAME = "raw"
    SYNOPSIS = "Issue an HTTP request to a Qumulo REST endpoint. Content "  \
               "for modifying requests (i.e. PATCH, POST, and PUT) can be " \
               "provided on stdin.  Output is provided on stdout."

    @staticmethod
    def options(parser):
        parser.add_argument(
            'method',
            choices=['DELETE', 'GET', 'PATCH', 'POST', 'PUT'],
            help='HTTP method. PATCH, POST, and PUT accept input on stdin')
        parser.add_argument('url', help='REST endpoint (e.g. /v1/ad/join)')
        parser.add_argument(
            '--content-type',
            choices=['application/json', 'application/octet-stream'],
            default='application/json',
            help='Content MIME type. Use application/octet-stream for binary '
                 'input. (Default: application/json)')

    @staticmethod
    def main(conninfo, credentials, args):
        body = None
        body_file = None
        if args.method in ['PATCH', 'POST', 'PUT']:
            if args.content_type == 'application/json':
                body = json.loads(sys.stdin.read())
            elif args.content_type == 'application/octet-stream':
                body_file = sys.stdin

        request.rest_request(
            conninfo,
            credentials,
            args.method,
            args.url,
            body=body,
            body_file=body_file,
            request_content_type=args.content_type,
            response_file=sys.stdout)
        sys.stdout.write('\n')
