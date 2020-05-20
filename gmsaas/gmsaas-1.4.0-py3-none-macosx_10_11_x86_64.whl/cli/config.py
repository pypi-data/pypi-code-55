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
Cli for subcommand config
"""
import os
from urllib.parse import urlparse

import click

from gmsaas.gmsaas.logger import echo_info
from gmsaas.storage import configcache as cfg

VALID_KEYS = sorted([cfg.SDK_PATH_KEY, cfg.PROXY_KEY])


class ConfigParamType(click.ParamType):
    """
    Validate value depending on which config key is stored
    """

    name = "config_param"

    def convert(self, value, param, ctx):
        if value == "":
            # No parsing check, settings will be reset
            return value

        key = ctx.params["entry"]
        if key == cfg.SDK_PATH_KEY:
            if not os.path.exists(value):
                self.fail("Path '{}' does not exist.".format(value))
        elif key == cfg.PROXY_KEY:
            error_str = "Invalid URL '{}', format should be '(http[s]|socks5)://[user[:password]@]host:port'.".format(
                value
            )
            try:
                url = urlparse(value)
            except Exception:
                self.fail(error_str)
            url_ok = all([url.scheme, url.hostname, url.port])
            if not url_ok:
                self.fail(error_str)
            if url.scheme.lower() not in ["http", "https", "socks5"]:
                self.fail(error_str)
        return value


@click.group()
def config():
    """
    Manage gmsaas configuration properties
    """


@click.command("set")
@click.argument("entry", type=click.Choice(VALID_KEYS))
@click.argument("value", type=ConfigParamType())
def config_set(entry, value):
    """
    Set a gmsaas configuration property

    \b
    android-sdk-path    Android SDK path
    proxy               URL of HTTP/HTTPS/SOCKS5 proxy server
                        For an authenticated proxy, credentials
                        can be included in the URL or set through
                        GMSAAS_PROXY_USERNAME and GMSAAS_PROXY_PASSWORD
                        environment variables.
    """
    cfg.set_config(entry, value)


@click.command("get")
@click.argument("entry", type=click.Choice(VALID_KEYS))
def config_get(entry):
    """
    Print a gmsaas configuration property

    \b
    android-sdk-path    Android SDK path
    proxy               URL of HTTP/HTTPS/SOCKS5 proxy server
    """
    echo_info(str(cfg.get_config(entry)))


@click.command("list")
def config_list():
    """
    List all gmsaas configuration properties
    """
    props = cfg.get_all()
    output = []
    for key in sorted(set(props.keys()).union(VALID_KEYS)):
        value = props.get(key, "")
        output.append("{}={}".format(key, value))
    echo_info("\n".join(output))


config.add_command(config_set)
config.add_command(config_get)
config.add_command(config_list)
