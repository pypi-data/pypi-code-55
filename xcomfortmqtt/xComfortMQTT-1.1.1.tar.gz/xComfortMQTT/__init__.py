#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
import click_log
import logging
import sys
from .xComforMqtt import xComforMqtt
from .config import load_config

__version__ = '1.1.1'


@click.command()
@click.version_option(version=__version__)
@click.option('--config', '-c', 'config_file', type=click.File('r'), required=True, help='configuration file (YAML format).')
@click_log.simple_verbosity_option(default='INFO')
def cli(config_file):
    logging.info('Process started')
    config = load_config(config_file)
    try:
        service = xComforMqtt(config)
        service.start()
    except KeyboardInterrupt as e:
        logging.warn('KeyboardInterrupt')

    logging.info('Process stopped')


def main():
    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
        cli()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        click.echo(str(e), err=True)
        if "DEBUG" in sys.argv:
            raise e
        sys.exit(1)
