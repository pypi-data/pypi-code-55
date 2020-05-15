#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: powermolecli.py
#
# Copyright 2020 Vincent Schouten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for powermolecli.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import argparse
import logging.config
from time import sleep
import coloredlogs
import pexpect
from powermolelib import (Configuration,
                          StateManager,
                          Heartbeat,
                          start_application,
                          write_ssh_config_file,
                          TransferAgent,
                          Tunnel,
                          ForAssistant,
                          TorAssistant,
                          InteractiveAssistant,
                          FileAssistant,
                          BootstrapAgent)
from powermolelib.powermolelibexceptions import InvalidConfigurationFile
from .lib import setup_link
from .powermolecliexceptions import SetupFailed

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''12-05-2020'''
__copyright__ = '''Copyright 2020, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''minitorcli'''  # non-class objects like functions can consult this Logger object
LOGGER = logging.getLogger(LOGGER_BASENAME)
# LOGGER.addHandler(logging.NullHandler())  # method not in https://docs.python.org/3/library/logging.html

# Constants
LOCAL_PATH_SSH_CFG = '/tmp/ssh_cfg_minitor'  # path to custom config file for ssh (generated by write_ssh_config_file())
LOCAL_HEARTBEAT_PORT = 11600  # local port used by the heartbeat mechanism to communicate with the last Machine
LOCAL_PROXY_PORT = 8080  # local port used to forward web traffic which exits last host (only in TOR mode)
LOCAL_TRANSFER_PORT = 11700  # local port used to upload files to last host (only in FILE mode)
LOCAL_COMMAND_PORT = 11800  # local port used to send linux commands to last host (only in INTERACTIVE mode)
MACHINE_DEPLOY_PATH = '/tmp/'  # path on last host where the agent will be transferred to
DEBUG = False  # to capture the output of the child (SSH), experimental


def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='''minitor - anonymizing internet traffic using private servers (cli)''')
    parser.add_argument('--config-file',
                        '-c',
                        help='The location of the config file',
                        dest='config_file',
                        action='store',
                        default='')
    parser.add_argument('--log-level',
                        '-L',
                        help='Provide the log level. Defaults to info.',
                        dest='log_level',
                        action='store',
                        default='info',
                        choices=['debug',
                                 'info',
                                 'warning',
                                 'error',
                                 'critical'])
    args = parser.parse_args()
    return args


def parse_config_file(config_file_path):
    """Parses the configuration file to a (dictionary) object."""
    try:
        configuration = Configuration(config_file_path)
    except InvalidConfigurationFile:
        return None
        # raise SystemExit(1)  # to keep it 'consistent' w/ develop design (powermolegui), no SystemExit() can be raised
    if configuration.mode == 'FILE':
        LOGGER.info('mode FILE enabled')
    elif configuration.mode == 'INTERACTIVE':
        LOGGER.info('mode INTERACTIVE enabled')
    elif configuration.mode == 'FOR':
        LOGGER.info('mode FOR enabled')
    elif configuration.mode == 'TOR':
        LOGGER.info('mode TOR enabled')
    return configuration


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    coloredlogs_format = '%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s'
    coloredlogs.install(fmt=coloredlogs_format, level=args.log_level.upper())
    config = parse_config_file(args.config_file)
    if not config:
        return None
    try:
        with StateManager() as state:
            write_ssh_config_file(LOCAL_PATH_SSH_CFG, config.gateways, config.destination)
            transferagent = TransferAgent(LOCAL_PATH_SSH_CFG, config.all_hosts)
            if config.mode == 'FOR':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts, config.forwarders_string)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = ForAssistant(tunnel)
            elif config.mode == 'TOR':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = TorAssistant(tunnel, '0.0.0.0')
            elif config.mode == 'FILE':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = FileAssistant(tunnel, LOCAL_TRANSFER_PORT)
            elif config.mode == 'INTERACTIVE':
                tunnel = Tunnel(LOCAL_PATH_SSH_CFG, config.mode, config.all_hosts)
                bootstrapagent = BootstrapAgent(tunnel, MACHINE_DEPLOY_PATH)
                assistant = InteractiveAssistant(tunnel, LOCAL_COMMAND_PORT)
            else:  # superfluous, the conditions will always be met
                SystemExit(1)
            setup_link(state, transferagent, tunnel, bootstrapagent, assistant, debug=DEBUG)
            with Heartbeat(LOCAL_HEARTBEAT_PORT):
                if config.mode == 'FOR':
                    LOGGER.info('connections on local ports %s will be forwarded', config.forwarders_ports)
                    LOGGER.info('READY')
                elif config.mode == 'TOR':
                    LOGGER.info('local port %s will be listening for web traffic', LOCAL_PROXY_PORT)
                    LOGGER.info('READY')
                elif config.mode == 'INTERACTIVE':
                    LOGGER.warning('the interface does not support shell meta characters ')
                    LOGGER.warning('such as pipe and it\'s not possible to interact with ')
                    LOGGER.warning('programs that need a response. hit control-c to quit')
                    try:
                        while True:
                            command = input('enter command: ')
                            response_raw = assistant.exec_command(command)
                            response_str = response_raw.decode("utf-8")
                            response_line = response_str.split('\n')
                            for line in response_line:
                                print('>    %s' % line)
                    except KeyboardInterrupt:
                        raise SystemExit(0)
                elif config.mode == 'FILE':
                    assistant.transfer(metadata_files=config.files)
                    raise SystemExit(0)
                else:  # superfluous, the conditions will always be met
                    SystemExit(1)
                if config.application:
                    LOGGER.info('starting application...')
                    process = start_application(binary_name=config.application['binary_name'],
                                                binary_location=config.application['binary_location'])
                    try:
                        while True:
                            sleep(1)
                    except KeyboardInterrupt:
                        process.terminate()
                        raise SystemExit(0)
                while True:
                    if DEBUG:
                        LOGGER.warning('debugging mode enabled')
                        tunnel.debug()  # blocking!
                        # raise KeyboardInterrupt
                    tunnel.child.expect([pexpect.TIMEOUT], timeout=1)  # purge child's output due to limited buffer
                    sleep(2)
    except SetupFailed as msg:
        # custom exception is defined in "minitorcliexceptions" and can only be raised by setup_link() in
        # the helpers module. the exception is raised when an object (eg. TransferAgent, Tunnel, Assistant)
        # cannot be started (start()) successfully.
        LOGGER.error(msg)
        raise SystemExit(1)
