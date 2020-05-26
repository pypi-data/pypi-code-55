# -*- coding: utf-8 -*-
import os
import yaml

from collections import OrderedDict

from .exceptions import ODRouteConfigException

DEFAULT_CONFIG = {
    'name': None,
    'source_info': [],
    'destinations': [],
    'edi_destinations': [],
    'nodata_failover_delay': 0.5,
    'nodata_recover_delay': 5,
    'noaudio_failover_delay': 10,
    'noaudio_recover_delay': 10,
    'audio_threshold': -90,
    'socket': None,
    'log_level': 'INFO',
    'log_format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
}


def load_config_file(path):
    if not os.path.exists(path):
        raise IOError('Config file does not exist: {}'.format(path))

    with open(path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    if not config:
        raise ODRouteConfigException('Unable to read configuration from file')

    parsed_config = parse_config(config)
    parsed_config['config_file'] = path

    return parsed_config

def parse_cli_args(cli_args):
    config = {}
    config.update(DEFAULT_CONFIG)

    config['source_info'] = []

    for port in cli_args.zmq_source_ports:
        config['source_info'].append({"protocol": "zmq", "port": port})

    for port in cli_args.edi_source_ports:
        config['source_info'].append({"protocol": "edi", "port": port})

    config['destinations'] = [{"protocol": "zmq", "endpoint": dest} for dest in cli_args.destinations]

    for dest in cli_args.edi_destinations:
        host, _, port = dest.partition(":")
        port = int(port)
        config['destinations'].append({"protocol": "edi", "host": host, "port": port})

    for k in ['name', 'nodata_failover_delay', 'nodata_recover_delay',
            'noaudio_failover_delay', 'noaudio_recover_delay', 'audio_threshold', 'socket']:
        config[k] = getattr(cli_args, k)

    return config


def parse_config(config):
    parsed_config = OrderedDict()

    defaults = OrderedDict(sorted(DEFAULT_CONFIG.items()))

    for key, value in defaults.items():
        """
        kind of ugly handling. make sure to apply default values if config file has
        keys set to 'none' - like:
            ...
            source_info:
              - {protocol: zmq, port: 10002}
            destinations:
            edi_destinations:
            nodata_failover_delay: 1.0
            ...
        """
        _value = config.get(key, value)
        if not _value:
            _value = value

        parsed_config[key] = _value

    # handle logging config
    parsed_config['log_level'] = parsed_config['log_level'].upper()

    if parsed_config['name']:
        parsed_config['log_format'] = 'odroute-{} {}'.format(parsed_config['name'], parsed_config['log_format'])

    if parsed_config['socket']:
        parsed_config['socket'] = os.path.abspath(parsed_config['socket'])

    return parsed_config
