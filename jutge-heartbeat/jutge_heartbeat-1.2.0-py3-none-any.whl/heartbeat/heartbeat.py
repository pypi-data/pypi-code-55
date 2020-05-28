#!/usr/bin/env python3

"""
Heartbeat for worker machines in Jutge.org.
"""

import argparse
import datetime
import http
import json
import logging
import os
import sys
import time

import requests
from jutge.monitor import monitor


def pulse(url, include_monitor_information, show=False):
    logging.info('pulse')

    last_pulse = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    data = {'last_pulse': last_pulse}

    if include_monitor_information:
        logging.info('monitor')
        data['last_monitor'] = monitor.information()

    if show:
        logging.info('json=%s', json.dumps(data))

    response = requests.patch(url, json=data)

    if response.status_code != http.HTTPStatus.OK:
        logging.warning('response-code=%d', response.status_code)


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=os.environ.get('LOGLEVEL', 'INFO'))

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Heartbeat for worker machines in Jutge.org',
        epilog='''
            For security reasons, the url to post heartbeat pulses 
            must be stored in the HEARTBEAT_URL environment variable.
            For example, set HEARTBEAT_URL=http://user:password@localhost:8000/api/machines/machine/
            specifying the protocol, the authentication credentials, the destination host
            and the name of your machine.

            You may also set the LOGLEVEL environment variable in order to 
            configure logging messages. Possibles values are DEBUG, INFO, WARNING,
            ERROR, CRITICAL.
            ''')
    parser.add_argument(
        '--period',
        type=int,
        help='how often to send the pulse, in seconds',
        default=5)
    parser.add_argument(
        '--monitor',
        type=int,
        help='how often to send the monitor, in pulses',
        default=12)
    parser.add_argument(
        '--times',
        type=int,
        help='number of times to repeat the pulse (default = forever)',
        default=-1)
    parser.add_argument(
        '--show',
        help='show the json message to send',
        action='store_true')
    args = parser.parse_args()

    url = os.environ.get('HEARTBEAT_URL', None)
    if url is None:
        logging.error('error=HEARTBEAT_URL variable not set')
        sys.exit(1)

    forever = args.times < 0
    i = 0
    while forever or i < args.times:
        try:
            pulse(url, i % args.monitor == 0, args.show)
        except Exception as e:
            logging.error('exception=%s', type(e).__name__)
        if forever or i < args.times - 1:
            time.sleep(args.period)
        i = i + 1


if __name__ == '__main__':
    main()
