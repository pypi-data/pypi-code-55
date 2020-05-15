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
from __future__ import print_function
from __future__ import unicode_literals

import warnings

import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.rest.audit as audit

from qumulo.lib.opts import str_decode

#                _
#  ___ _   _ ___| | ___   __ _
# / __| | | / __| |/ _ \ / _` |
# \__ \ |_| \__ \ | (_) | (_| |
# |___/\__, |___/_|\___/ \__, |
#      |___/             |___/
#  FIGLET: syslog
#

class GetAuditLogSyslogConfig(qumulo.lib.opts.Subcommand):
    NAME = 'audit_get_syslog_config'
    SYNOPSIS = 'Get audit syslog server configuration'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(audit.get_syslog_config(conninfo, credentials))

class SetAuditLogSyslogConfig(qumulo.lib.opts.Subcommand):
    NAME = 'audit_set_syslog_config'
    SYNOPSIS = 'Change audit syslog server configuration'

    @staticmethod
    def options(parser):
        enabled_group = parser.add_mutually_exclusive_group(required=False)
        enabled_group.set_defaults(enabled=None)
        enabled_group.add_argument(
            '--enable',
            '-e',
            dest='enabled',
            action='store_true',
            help='Enable audit log.')
        enabled_group.add_argument(
            '--disable',
            '-d',
            dest='enabled',
            action='store_false',
            help='Disable audit log.')

        parser.add_argument(
            '--server-address',
            '-s',
            type=str_decode,
            help=('The IP address, hostname, or fully qualified domain name of '
                'your remote syslog server.'))

        parser.add_argument(
            '--server-port',
            '-p',
            type=int,
            help='The port to connect to on your remote syslog server.')

    @staticmethod
    def main(conninfo, credentials, args):
        print(audit.set_syslog_config(
            conninfo,
            credentials,
            enabled=args.enabled,
            server_address=args.server_address,
            server_port=args.server_port))

class GetAuditLogSyslogStatus(qumulo.lib.opts.Subcommand):
    NAME = 'audit_get_syslog_status'
    SYNOPSIS = 'Get audit syslog server status'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(audit.get_syslog_status(conninfo, credentials))

#       _                 _               _       _
#   ___| | ___  _   _  __| |_      ____ _| |_ ___| |__
#  / __| |/ _ \| | | |/ _` \ \ /\ / / _` | __/ __| '_ \
# | (__| | (_) | |_| | (_| |\ V  V / (_| | || (__| | | |
#  \___|_|\___/ \__,_|\__,_| \_/\_/ \__,_|\__\___|_| |_|
#  FIGLET: cloudwatch
#

class GetAuditLogCloudwatchConfig(qumulo.lib.opts.Subcommand):
    NAME = 'audit_get_cloudwatch_config'
    SYNOPSIS = 'Get audit CloudWatch configuration'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(audit.get_cloudwatch_config(conninfo, credentials))

class SetAuditLogCloudwatchConfig(qumulo.lib.opts.Subcommand):
    NAME = 'audit_set_cloudwatch_config'
    SYNOPSIS = 'Change audit CloudWatch configuration'

    @staticmethod
    def options(parser):
        enabled_group = parser.add_mutually_exclusive_group(required=False)
        enabled_group.set_defaults(enabled=None)
        enabled_group.add_argument(
            '--enable',
            '-e',
            dest='enabled',
            action='store_true',
            help='Enable audit log.')
        enabled_group.add_argument(
            '--disable',
            '-d',
            dest='enabled',
            action='store_false',
            help='Disable audit log.')

        parser.add_argument(
            '-l',
            '--log-group-name',
            type=str_decode,
            help='The group name in CloudWatch Logs to send logs to.')
        parser.add_argument(
            '-r',
            '--region',
            type=str_decode,
            help='The AWS region to send logs to.')

    @staticmethod
    def main(conninfo, credentials, args):
        print(audit.set_cloudwatch_config(
            conninfo,
            credentials,
            enabled=args.enabled,
            log_group_name=args.log_group_name,
            region=args.region))

class GetAuditLogCloudwatchStatus(qumulo.lib.opts.Subcommand):
    NAME = 'audit_get_cloudwatch_status'
    SYNOPSIS = 'Get audit CloudWatch status'

    @staticmethod
    def main(conninfo, credentials, _args):
        print(audit.get_cloudwatch_status(conninfo, credentials))

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

class GetAuditLogConfig(qumulo.lib.opts.Subcommand):
    NAME = 'audit_get_config'
    SYNOPSIS = 'DEPRECATED: command has moved to audit_get_syslog_config.'

    @staticmethod
    def main(conninfo, credentials, args):
        warnings.warn(
            "audit_get_config is deprecated, "
            "use audit_get_syslog_config instead",
            DeprecationWarning)
        GetAuditLogSyslogConfig.main(conninfo, credentials, args)

class SetAuditLogConfig(qumulo.lib.opts.Subcommand):
    NAME = 'audit_set_config'
    SYNOPSIS = 'DEPRECATED: command has moved to audit_set_syslog_config.'

    @staticmethod
    def options(parser):
        enabled_group = parser.add_mutually_exclusive_group(required=False)
        enabled_group.set_defaults(enabled=None)
        enabled_group.add_argument(
            '--enable',
            '-e',
            dest='enabled',
            action='store_true',
            help='Enable audit log.')
        enabled_group.add_argument(
            '--disable',
            '-d',
            dest='enabled',
            action='store_false',
            help='Disable audit log.')

        parser.add_argument(
            '--server-address',
            '-s',
            type=str_decode,
            help=('The IP address, hostname, or fully qualified domain name of '
                'your remote syslog server.'))

        parser.add_argument(
            '--server-port',
            '-p',
            type=int,
            help='The port to connect to on your remote syslog server.')

    @staticmethod
    def main(conninfo, credentials, args):
        warnings.warn(
            "audit_set_config is deprecated, "
            "use audit_set_syslog_config instead",
            DeprecationWarning)
        SetAuditLogSyslogConfig.main(conninfo, credentials, args)

class GetAuditLogStatus(qumulo.lib.opts.Subcommand):
    NAME = 'audit_get_status'
    SYNOPSIS = 'DEPRECATED: command has moved to audit_set_syslog_status.'

    @staticmethod
    def main(conninfo, credentials, args):
        warnings.warn(
            "audit_get_status is deprecated, "
            "use audit_get_syslog_status instead",
            DeprecationWarning)
        GetAuditLogSyslogStatus.main(conninfo, credentials, args)
