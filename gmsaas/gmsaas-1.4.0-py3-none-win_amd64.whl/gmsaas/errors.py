# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
gmsaas errors
"""
import json
import shlex
import sys

from enum import Enum
import click
from gmsaas.gmsaas.logger import LOGGER
from gmsaas.model.instanceinfo import InstanceState, is_instance_starting, is_instance_stopping
import gmsaas


class ExitCode(Enum):
    """
    Exit codes used by gmsaas
    """

    NO_ERROR = 0
    DEFAULT_ERROR = 1  # Default of ClickException class
    USAGE_ERROR = 2  # Used by click's UsageError class
    AUTHENTICATION_ERROR = 3
    API_ERROR = 4
    INVALID_JSON_ERROR = 5
    CONFIGURATION_ERROR = 6
    PACKAGE_ERROR = 7
    COMPATIBILITY_ERROR = 8
    UNREACHABLE_ERROR = 9
    INSTANCE_ERROR = 10
    ADBTUNNEL_BUSY_PORT_ERROR = 11
    ADBTUNNEL_GENERIC_ERROR = 12
    ADBTUNNEL_DIFFERENT_PORT_ERROR = 13
    ADBTUNNEL_INSTANCE_NOT_READY = 14
    REQUEST_ERROR = 15
    LOGZIP_ERROR = 16


class ApiErrorCode:
    """
    Error codes return by the API
    """

    BAD_USERNAME_PASSWORD = "BAD_USERNAME_PASSWORD"
    USER_NOT_ENABLED = "USER_NOT_ENABLED"


class GmsaasError(click.ClickException):
    """
    Base class for every `gmsaas` errors (except for errors occuring before logging setup)
    Note: Make sure to update `show_gmsaas_outputs` when something changes
    """

    def __init__(self, exit_code, message, extra_logged_message=None, show_verbose_hint=False):
        super().__init__(message)
        self.exit_code = exit_code
        self.extra_logged_message = extra_logged_message
        self.show_verbose_hint = show_verbose_hint and not LOGGER.is_verbose

    def show(self, file=None):
        """
        Print exception in stderr

        If `show_verbose_hint` is True, the failing command is printed with the verbose flag.
        Exception message is also logged as well as `extra_logged_message` and exit code.
        """
        LOGGER.error(self.message)
        if self.extra_logged_message:
            LOGGER.error(self.extra_logged_message)
        LOGGER.info("==== STOP exit code: %d (%s) ====", self.exit_code, ExitCode(self.exit_code))
        output = self.message
        if self.show_verbose_hint:
            args = [gmsaas.__application__, "--verbose"]
            args.extend(sys.argv[1:])
            cmd = " ".join(shlex.quote(x) for x in args)
            output += "\nUse '{}' for more information.".format(cmd)
        click.echo(output, err=True)


class AuthenticationError(GmsaasError):
    """
    Authentication Error
    """

    def __init__(self, status_code, message):
        output_message = "Error: {} {}".format(status_code, message)
        try:
            response = json.loads(message)
            code = response.get("code")
            if code == ApiErrorCode.BAD_USERNAME_PASSWORD:
                output_message = "Error: create an account or retrieve your password at https://cloud.geny.io."
            elif code == ApiErrorCode.USER_NOT_ENABLED:
                output_message = "Error: your account is disabled. Please contact your organization administrator."
        except Exception:
            pass

        super().__init__(ExitCode.AUTHENTICATION_ERROR.value, output_message)


class ApiError(GmsaasError):
    """
    API Error (wrong HTTP code)
    """

    def __init__(self, status_code, message):
        super().__init__(
            ExitCode.API_ERROR.value, "API return unexpected code: {}. Error: {}".format(status_code, message)
        )


class InvalidJsonError(GmsaasError):
    """
    Invalid JSON Error
    """

    def __init__(self, status_code, message):
        super().__init__(
            ExitCode.INVALID_JSON_ERROR.value, "API return invalid JSON: {}. Error: {}".format(status_code, message)
        )


class NoCredentialsError(GmsaasError):
    """
    Config Error
    """

    def __init__(self):
        super().__init__(
            ExitCode.CONFIGURATION_ERROR.value, "Error: no credentials found. To set them up, use 'gmsaas auth login'."
        )


class NoAndroidToolsError(GmsaasError):
    """
    Config Error
    """

    def __init__(self):
        super().__init__(
            ExitCode.CONFIGURATION_ERROR.value,
            "Error: no Android SDK path set. To set it up, use 'gmsaas config set android-sdk-path <path>'.",
        )


class PackageError(GmsaasError):
    """
    Package Error
    """

    def __init__(self):
        super().__init__(
            ExitCode.PACKAGE_ERROR.value,
            "Error: 'gmsaas' seems corrupted, try to re-install it.",
            "Unable to execute gmadbtunneld binary embedded in package",
        )


class MismatchedVersionError(GmsaasError):
    """
    Mismatched version Error
    """

    def __init__(self, gmsaas_version, adbtunnel_version):
        self.gmsaas_version = gmsaas_version
        self.adbtunnel_version = adbtunnel_version
        super().__init__(
            ExitCode.COMPATIBILITY_ERROR.value,
            "Error: incompatible version numbers.\n"
            "gmadbtunneld version is '{}'.\n"
            "gmsaas version is '{}'.\n"
            "Please use same version numbers, or kill 'gmadbtunneld'.".format(adbtunnel_version, gmsaas_version),
        )


class MismatchedPlatformUrlError(GmsaasError):
    """
    Mismatched platform url Error
    """

    def __init__(self, gmsaas_platform_url, adbtunnel_platform_url):
        self.gmsaas_platform_url = gmsaas_platform_url
        self.adbtunnel_platform_url = adbtunnel_platform_url
        super().__init__(
            ExitCode.COMPATIBILITY_ERROR.value,
            "Error: inconsistent server URLs.\n"
            "gmadbtunneld connects to '{}'.\n"
            "gmsaas connects to '{}'.\n"
            "Please use same server URLs, or kill 'gmadbtunneld'.".format(adbtunnel_platform_url, gmsaas_platform_url),
        )


class MismatchedProxyError(GmsaasError):
    """
    Mismatched proxy Error
    """

    def __init__(self, gmsaas_proxy, adbtunnel_proxy):
        self.gmsaas_proxy = gmsaas_proxy
        self.adbtunnel_proxy = adbtunnel_proxy
        super().__init__(
            ExitCode.COMPATIBILITY_ERROR.value,
            "Error: inconsistent proxies.\n"
            "gmadbtunneld uses '{}'.\n"
            "gmsaas uses '{}'.\n"
            "Please use same proxies, or kill 'gmadbtunneld'.".format(adbtunnel_proxy, gmsaas_proxy),
        )


class UnreachableError(GmsaasError):
    """
    Unreachable Error
    """

    def __init__(self, exception):
        super().__init__(
            ExitCode.UNREACHABLE_ERROR.value,
            "Error: unable to connect to Genymotion SaaS server",
            extra_logged_message=str(exception),
        )


def _get_instance_error(instance_uuid, expected_state, actual_state):
    assert expected_state in [InstanceState.ONLINE, InstanceState.DELETED], "Expected state is not subject to error"

    if expected_state == InstanceState.ONLINE:
        if is_instance_starting(actual_state):
            return "Error: instance '{}' did not start in time, please check its state with 'gmsaas instances list'".format(
                instance_uuid
            )
        elif is_instance_stopping(actual_state):
            return "Error: instance '{}' has been stopped".format(instance_uuid)
        return "Error: instance '{}' failed to start, please check its state with 'gmsaas instances list'".format(
            instance_uuid
        )

    if is_instance_stopping(actual_state):
        return "Error: instance '{}' did not stop in time, please check its state with 'gmsaas instances list'".format(
            instance_uuid
        )
    return "Error: instance '{}' failed to stop, please check its state with 'gmsaas instances list'".format(
        instance_uuid
    )


class InstanceError(GmsaasError):
    """
    Instance Error
    """

    def __init__(self, instance_uuid, expected_state, actual_state):
        super().__init__(
            ExitCode.INSTANCE_ERROR.value,
            _get_instance_error(instance_uuid, expected_state, actual_state),
            extra_logged_message="Instance '{}' expects to be '{}' but reached '{}'".format(
                instance_uuid, expected_state, actual_state
            ),
        )


class AdbTunnelBusyPortError(GmsaasError):
    """
    AdbTunnel Busy Port Error
    """

    def __init__(self, instance_uuid, port):
        super().__init__(
            ExitCode.ADBTUNNEL_BUSY_PORT_ERROR.value,
            "ADB tunnel communication failure. Port '{}' is not available.".format(port),
            extra_logged_message="Failed to connect instance {} to adbtunnel: port {} is busy".format(
                instance_uuid, port
            ),
        )


class AdbTunnelGenericError(GmsaasError):
    """
    AdbTunnel Generic Error
    """

    def __init__(self, instance_uuid):
        super().__init__(
            ExitCode.ADBTUNNEL_GENERIC_ERROR.value,
            "ADB tunnel communication failure.",
            extra_logged_message="Failed to connect instance {} to adbtunnel".format(instance_uuid),
            show_verbose_hint=True,
        )


class AdbTunnelRunningOnDifferentPortError(GmsaasError):
    """
    AdbTunnel Running On Different Port
    """

    def __init__(self, instance_uuid, running_port, wanted_port):
        super().__init__(
            ExitCode.ADBTUNNEL_DIFFERENT_PORT_ERROR.value,
            "Instance already connected to ADB tunnel on port '{}'.".format(running_port),
            extra_logged_message="Instance {} cannot connect to adbtunnel with port {}: already connected on port {}".format(
                instance_uuid, wanted_port, running_port
            ),
        )


def _get_adbtunnel_instance_error(instance_uuid, instance_state):
    assert instance_state != InstanceState.ONLINE

    if instance_state == InstanceState.UNKNOWN:
        return "Error: instance '{}' does not exist.".format(instance_uuid)
    return "Error: instance '{}' is not started yet.".format(instance_uuid)


class AdbTunnelInstanceNotReadyError(GmsaasError):
    """
    AdbTunnel Instance Not Ready
    """

    def __init__(self, instance_uuid, instance_state):
        super().__init__(
            ExitCode.ADBTUNNEL_INSTANCE_NOT_READY.value,
            _get_adbtunnel_instance_error(instance_uuid, instance_state),
            extra_logged_message="Instance {} cannot connect to adbtunnel: state={}".format(
                instance_uuid, instance_state
            ),
        )


class RequestError(GmsaasError):
    """
    Request Error
    """

    def __init__(self, request_exception):
        super().__init__(
            ExitCode.REQUEST_ERROR.value,
            "Error: no network connection",
            extra_logged_message=str(request_exception),
            show_verbose_hint=True,
        )


class SSLError(GmsaasError):
    """
    SSL Error
    """

    def __init__(self, ssl_exception):
        super().__init__(
            ExitCode.REQUEST_ERROR.value,
            "Error: SSL failed",
            extra_logged_message=str(ssl_exception),
            show_verbose_hint=True,
        )


class ProxyError(GmsaasError):
    """
    Proxy Error
    """

    def __init__(self, request_exception):
        super().__init__(
            ExitCode.REQUEST_ERROR.value,
            "Error: unable to use the proxy",
            extra_logged_message=str(request_exception),
            show_verbose_hint=True,
        )


class LogzipError(GmsaasError):
    """
    Logzip Error
    """

    def __init__(self, logzip_exception):
        super().__init__(
            ExitCode.LOGZIP_ERROR.value,
            "Error: unable to generate logs archive",
            extra_logged_message=str(logzip_exception),
            show_verbose_hint=True,
        )
