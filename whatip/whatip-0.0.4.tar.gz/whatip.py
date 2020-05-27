import time
import re
from argparse import ArgumentParser
import sys
import logging
import socket
from queue import Queue, Empty
from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError

VERSION = '0.0.4'
SOURCES = ['ipapi', 'formyip']


def parse_cli():
    parser = ArgumentParser()
    parser.add_argument(
        '-a', '--address', action='store_true', default=False,
        help='display only IP address',
    )
    parser.add_argument(
        '-s', '--source', choices=SOURCES,
        help='use specific source',
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='enable debug output',
    )
    return parser.parse_args()


def request(url):
    try:
        return urlopen(url).read().decode('utf-8')
    except (HTTPError, OSError) as ex:
        logging.debug('Failed to process URL %s, reason: %s', url, ex)
        return None


def thread_formyip(resultq):
    data = request('http://formyip.com')
    if data:
        ok = False
        match = re.search(r'Your IP is ([^<]*)', data)
        if match:
            addr = match.group(1)
            match = re.search(r'Your Country is: ([^<]*)', data)
            if match:
                ok = True
                cnt = match.group(1)
                resultq.put({
                    'address': addr,
                    'country': cnt,
                })
        if not ok:
            logging.debug('Failed to parse formyip.com response')


def thread_ipapi(resultq):
    data = request('http://ip-api.com/json')
    if data:
        ok = False
        match = re.search(r'query":"(.+?)"', data)
        if match:
            addr = match.group(1)
            match = re.search(r'country":"(.+?)"', data)
            if match:
                ok = True
                cnt = match.group(1)
                resultq.put({
                    'address': addr,
                    'country': cnt,
                })
        if not ok:
            logging.debug('Failed to parse ip-api.com response')


def main():
    opts = parse_cli()
    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    if opts.source in SOURCES:
        sources = [opts.source]
    else:
        sources = SOURCES

    network_timeout = 5
    socket.setdefaulttimeout(network_timeout)
    resultq = Queue()
    pool = []
    for source in sources:
        th = Thread(
            target=globals()['thread_%s' % source],
            args=[resultq],
        )
        th.daemon = True
        th.start()
        pool.append(th)

    start = time.time()
    res = None
    while (time.time() - start) < network_timeout:
        try:
            res = resultq.get(True, 0.1)
        except Empty:
            if not any(x.isAlive() for x in pool):
                break
        else:
            break
    if not res:
        sys.stderr.write('Failed to parse external IP from all sources.\n')
        sys.exit(1)
    else:
        if opts.address:
            print(res['address'])
        else:
            print('%(address)s %(country)s' % res)


if __name__ == '__main__':
    main()
