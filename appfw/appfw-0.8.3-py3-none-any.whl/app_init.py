#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application script generator

Created on   : 2020-03-14 ( Ergin Soysal )
Last modified: May 10, 2020, Sun 12:49:10 -0500
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import os.path

import re
from datetime import datetime
import getpass

import argparse
from . import app


DEFAULT_APP_NAME = 'My App'
DEF_VARS = {
    'now': datetime.now().isoformat(timespec='seconds'),
    'author': getpass.getuser()
}

TPL_PATH = os.path.join(os.path.dirname(__file__), 'tpl')
APP_TPL = os.path.join(TPL_PATH, 'app.tpl')
CONF_TPL = os.path.join(TPL_PATH, 'config.tpl')

def normalize(name):
    normal_name = re.sub(r'\W+', '_', name.lower())
    normal_name = re.sub(r'(?:^_|_$)+', '', normal_name)

    return normal_name


def cleanup_filename(name):
    return re.sub(r'[^a-zA-Z0-9_.]+', '', name)


def get_app_name(def_val):
    app_name = input ( "Application name [%s]: " % DEFAULT_APP_NAME )
    return app_name if app_name else def_val


def get_app_filename(name):
    default_name = '%s.py' % name

    app_file = input ( "Application filename [%s]: " % default_name )

    return cleanup_filename(app_file) \
        if app_file else default_name


def get_conf_filename(name):
    default_name = '%s.cfg' % name

    conf_file = input ( "Configuration filename [%s]: " % default_name )
    return cleanup_filename(conf_file) \
        if conf_file else default_name


def get_log_filename(name):
    default_name = '%s.log' % name

    log_file = input ( "Log filename [%s]: " % default_name )

    return cleanup_filename(log_file) \
        if log_file else default_name


def read_file(fname):
    with open(fname, 'r') as fh:
        return fh.read()


def write_file(fname, content=''):
    with open(fname, 'w') as fh:
        fh.write(content)


def generate_file(out_name, tpl_name, vars=None):

    vars = DEF_VARS if not vars else {**DEF_VARS, **vars}
    tpl = read_file(tpl_name)
    content = tpl.format(**vars)
    write_file(out_name, content)


def build(args):
    # Application name
    app_name = args.app_name or get_app_name(DEFAULT_APP_NAME)

    # Default names
    normal_name = normalize(app_name)

    app_file = args.app_file or get_app_filename(normal_name)
    conf_file = args.app_conf_file or get_conf_filename(normal_name)
    log_file = args.app_log_file or get_log_filename(normal_name)
    log_section = args.app_log_section or 'log'

    vars = {'log_file': log_file, 'app_name': app_name,
            'log_section':log_section, 'normal_name': normal_name,
            'conf_file': conf_file}

    app.info('Generating application file %s', app_file)
    generate_file(app_file, APP_TPL, vars)

    app.info('Generating configuration file %s', conf_file)
    generate_file(conf_file, CONF_TPL, vars)


def main(args, config):
    try:
        build(args)
    except Exception as e:
        # raise_with_traceback(e)
        app.exception(e)


def parse_args():
    parser = argparse.ArgumentParser(description='''Application script generator''')
    parser.add_argument('-c', '--cfgfile', default='appl.cfg',
                            type=str, help='Configuration file')
    parser.add_argument('--log-section', default='log', type=str,
                        help='Log section name in the configuration file')
    parser.add_argument('-o', '--output', default='.', help='Output folder')
    parser.add_argument('-n', '--app-name', default=None,
                        help='Application name')
    parser.add_argument('-af', '--app-file', default=None,
                        help='Application filename')
    parser.add_argument('-cf', '--app-conf-file', default=None,
                        help='Configuration filename')
    parser.add_argument('-lf', '--app-log-file', default=None,
                        help='Log filename')
    parser.add_argument('-ls', '--app-log-section', default=None,
                        help='Log configuration section name')

    return parser.parse_args()


def run():
    args = parse_args()
    config = app.configure(args)
    main(args, config)


if __name__ == '__main__':
    run()


