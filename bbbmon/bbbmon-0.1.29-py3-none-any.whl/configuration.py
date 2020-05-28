#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
from typing import NewType, Optional, Tuple, Iterable, List
import click
import os

# Default path
SERVER_PROPERTIES_FILE = "/usr/share/bbb-web/WEB-INF/classes/bigbluebutton.properties"


# Type definitions
Secret = NewType('Secret', str)
Url    = NewType('Url', str)


EXAMPLE_CONFIG = """[myservername]
securitySalt=YOURSUPERSECRETSECRET
bigbluebutton.web.serverURL=https://bbb.example.com/

; You can add, however, multiple Endpoints:
; [mysecondservername]
; securitySalt=ANOTHERSECRET
; bigbluebutton.web.serverURL=https://bbb.test.com/
"""



class Config():
    """
    Holds the Server Configurations for multiple endpoints
    """
    def __init__(self):
        self.endpoints = []
        self.path = None
        self.on_server = None

    def from_server(self, path: str=SERVER_PROPERTIES_FILE) -> 'Config':
        """
        If bbbmon is executed on the server, it uses this method to extract the
        Url (bigbluebutton.web.serverURL) and the Secret (securitySalt) from the
        server. Additionally this method is used as a legacy fallback for user
        configuration files that are not a valid ini with [section headers]
        """
        with open(path, "r") as f:
            lines = [l for l in f.readlines()]
            secret = Secret([l for l in lines if l.startswith("securitySalt=")][0].replace("securitySalt=", "")).strip()
            bbb_url = Url([l for l in lines if l.startswith("bigbluebutton.web.serverURL=")][0].replace("bigbluebutton.web.serverURL=", "")).strip()
            bbb_url = "{}/bigbluebutton".format(bbb_url.rstrip('/'))
            endpoint = Endpoint(url=bbb_url, secret=secret)
            self.endpoints.append(endpoint)
            self.path = path
        self.on_server = True
        return self

    def from_config(self, path: str) -> 'Config':
        """
        Read config from a given path. If the file has no section headers, try
        to use the .from_server(path) method instead
        """
        config = configparser.ConfigParser()
        try:
            config.read(path, encoding='utf-8')
            for section in config.sections():
                bbb_url = Url(config[section]["bigbluebutton.web.serverURL"])
                bbb_url = "{}/bigbluebutton".format(bbb_url.rstrip('/'))
                secret = Secret(config[section]["securitySalt"]).strip()
                endpoint = Endpoint(url=bbb_url, secret=secret, name=section)
                self.endpoints.append(endpoint)
                self.path = path
            self.on_server = False
            return self
        # Fallback for config files without sections
        except configparser.MissingSectionHeaderError:
            self = self.from_server(path)
            self.on_server = False
            return self

    def filter_endpoints(self, endpoint_options: List[str]) -> 'Config':
        """
        Return a Config that only contains the matching endpoints. If the endpoint
        isn't found, return a Error message.
        """
        if len(endpoint_options) == 0:
            return self
        else:
            existing_names = [e.name for e in self.endpoints]
            filtered_endpoints = []
            for endpoint_option in endpoint_options:
                if not endpoint_option in existing_names:
                    click.echo("{} there is no endpoint called \"{}\" in the configuration. It will be ignored.\n".format(click.style('Error:', fg='red', bold=True), click.style(endpoint_option, fg='red', bold=True)))
                    if self.on_server:
                        click.echo("{} bbbmon is using the server config. You can use a user config using the {} flag.\n".format(click.style('Hint:', fg='yellow', bold=True), click.style("--userconfig", fg='bright_black', bold=True)))
                    if len(self.endpoints) > 0:
                        click.echo("{}".format(click.style('Available Endpoints:', fg='green', bold=True)))
                        for endpoint in self.endpoints:
                            click.echo("    → {}".format(click.style(endpoint.name, fg='green', bold=True)))

                else:
                    filtered_endpoints.append([e for e in self.endpoints if e.name == endpoint_option][0])

            self.endpoints = filtered_endpoints
            return self


    def __len__(self):
        """
        The length of a Config is represented by the number of endpoints
        """
        return len(self.endpoints)

    def __str__(self):
        """
        Allow a Config to be represented by a string quickly
        """
        l = ["Config"]
        for e in ["Endpoint[{}]: {}, SECRET OMITTED".format(e.name, e.url) for e in self.endpoints]:
            l.append(e)
        return "\n".join(l)




class Endpoint():
    """
    Objects of this class represent a single endpoint which runs a bigbluebutton
    instance. The relevant fields are the url and the secret, the name is either
    extracted from the section header of the user configuration file, or – as a
    fallback – from the URL
    """
    def __init__(self, url: Url, secret: Secret, name: str=None):
        self.url = url
        self.secret = secret
        if name is None:
            self.name = url.lower()\
                           .lstrip("http://")\
                           .lstrip("https://")\
                           .rstrip("/bigbluebutton")
        else:
            self.name = name


def init_config(userconfig: bool) -> Optional[Config]:
    """
    Read the config either from the servers bigbluebutton.properties-file or from
    the user config path. Display a message if neither of these files exist.
    """
    # Get OS dependend properties file
    user_config_path = get_user_config_path()

    # Check if we are on the server and try to read that properties file first
    if os.path.isfile(SERVER_PROPERTIES_FILE) and not userconfig:
        return Config().from_server()
    elif os.path.isfile(user_config_path):
        return Config().from_config(user_config_path)
    else:
        new_config(user_config_path)


def new_config(user_config_path: str, skip_prompt: bool=True):
    """
    Warn users that there was no config file found, and then ask them if they want to create one.
    The skip_prompt flag can be used to invoke this without asking or printing (e.g.
    if asking and printing should be done elsewhere)
    """
    if not skip_prompt:
        click.echo("{} There was no config file found. Make sure it exists and is readable at either location:".format(click.style('Error:', fg='red', bold=True), click.style("Error:", fg='red', bold=True)))
        print("       [0] {}".format(SERVER_PROPERTIES_FILE))
        print("       [1] {}".format(user_config_path))
        print()
        print("For now the file just needs to contain three lines:")
        for line in EXAMPLE_CONFIG.splitlines():
            click.echo(click.style((line), fg="bright_black"))
        print()

    if skip_prompt or click.confirm(click.style('Do you want to create a config file at {}?'.format(user_config_path), fg="green"), abort=True):
        # Create all directories in the path to the config, if they don't exist yet
        try:
            os.makedirs(user_config_path.rstrip("bbbmon.properties"))
        except FileExistsError:
            pass

        # Write default config
        with open(user_config_path, "w") as f:
            for line in EXAMPLE_CONFIG.splitlines():
                f.write("{}\n".format(line))

        # Open with standard editor
        click.edit(filename=user_config_path)

    exit()


def get_user_config_path() -> str:
    """
    Return the user config path
    """
    user_config_path = click.get_app_dir("bbbmon")
    user_config_path = "{}.properties".format(user_config_path)
    return user_config_path