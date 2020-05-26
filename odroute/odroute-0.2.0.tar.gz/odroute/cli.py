# -*- coding: utf-8 -*-
import logging
import os
import sys
import argparse

from .config import DEFAULT_CONFIG, parse_cli_args, load_config_file
from .router import StreamRouter
from .control.rcserver import RCServer

from odroute import __version__

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="ODR Stream Router")

    parser.add_argument('-v', '--verbose', action="store_true", help='Set log level to DEBUG')
    parser.add_argument('-c', '--config_file', type=str, help='Location of configuration file', required=False)
    parser.add_argument('-V', '--version', action="store_true", help='Show version')
    parser.add_argument('--name', default=DEFAULT_CONFIG['name'], help='Set name of this router for logging')

    # sources (a.k.a. inputs) and outputs
    parser.add_argument('-s', '--source', dest='zmq_source_ports', action="append", type=int, default=[],
                  help='The source ports for incoming ZMQ connections. Can be given multiple times'
                  )
    parser.add_argument('-e', '--edi-source', dest='edi_source_ports', action="append", type=int, default=[],
                  help='The source ports for incoming EDI connections. Can be given multiple times'
                  )
    parser.add_argument('-o', '--output', dest='destinations', action="append", type=str, default=[],
                  help='ZMQ Destinations to route to, in the form of: tcp://<hostname>:<port>. Can be given multiple times'
                  )
    parser.add_argument('-O', '--output-edi', dest='edi_destinations', action="append", type=str, default=[],
                  help='EDI Destinations to route to, in the form of: <hostname>:<port>. Can be given multiple times'
                  )

    # no-audio and no-data failovers
    parser.add_argument('-d', '--delay', dest='nodata_failover_delay', type=float,
                  default=DEFAULT_CONFIG['nodata_failover_delay'],
                  help='Delay for falling back to secondary streams in case of missing data'
                  )

    parser.add_argument('-r', '--delay-recover', dest='nodata_recover_delay', type=float,
                  default=DEFAULT_CONFIG['nodata_recover_delay'],
                  help='Delay for falling back to primary streams in case of recovery'
                  )

    parser.add_argument('-a', '--audio-threshold', dest='audio_threshold', type=int,
                  default=DEFAULT_CONFIG['audio_threshold'],
                  help='Minimum audio level (range [-90..0] dB) for input to be considered ok. Set to -90 to disable level detection'
                  )
    parser.add_argument('-D', '--audio-delay', dest='noaudio_failover_delay', type=int,
                  default=DEFAULT_CONFIG['noaudio_failover_delay'],
                  help='Delay for falling back to secondary streams in case of audio level below threshold'
                  )
    parser.add_argument('-R', '--audio-delay-recover', dest='noaudio_recover_delay', type=int,
                  default=DEFAULT_CONFIG['noaudio_recover_delay'],
                  help='Delay for falling back to primary streams in case of audio level recovery'
                  )
    # 'external' controls
    parser.add_argument('-S', '--socket', dest='socket', type=str,
                  default=DEFAULT_CONFIG['socket'],
                  help='Add unix datagram socket interface: </path/to/socket>'
                  )

    cli_args = parser.parse_args()

    if cli_args.version:
        print(__version__)
        sys.exit()

    if cli_args.config_file:
        config_file = os.path.abspath(cli_args.config_file)
        print('-' * 72)
        print('Using config file - other CLI options will be ignored.\nConfig: {}'.format(config_file))
        print('-' * 72)
        parsed_config = load_config_file(config_file)
    else:
        parsed_config = parse_cli_args(cli_args)


    # primitive logger configuration
    logging.basicConfig(
        format=parsed_config['log_format'],
        level=parsed_config['log_level'],
    )

    if cli_args.verbose:
        logger.setLevel(logging.DEBUG)

    while True:
        r = StreamRouter(config=parsed_config)

        # adding remote-control interface
        unix_socket = parsed_config.get('socket', None)
        if unix_socket:
            logger.info('Binding unix socket interface to {}'.format(unix_socket))
            rc_server = RCServer(r, unix_socket)
            r.register_rc(rc_server)
        try:
            r.start()
        except KeyboardInterrupt:
            logger.info('Ctrl-c received. Stopping router.')
            r.stop()
            sys.exit()

