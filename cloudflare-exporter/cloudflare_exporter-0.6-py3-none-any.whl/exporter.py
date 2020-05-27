import argparse
import logging
import sys

from aiohttp import web
from prometheus_client.core import REGISTRY

from cloudflare_exporter.collector import CloudflareCollector
from cloudflare_exporter.config import (DEFAULT_HOST,
                                        DEFAULT_LOGS_FETCH,
                                        DEFAULT_LOGS_COUNT,
                                        DEFAULT_LOGS_RANGE,
                                        DEFAULT_LOGS_SAMPLE,
                                        DEFAULT_PORT, LOG_FORMAT)
from cloudflare_exporter.handlers import handle_health, handle_metrics


def parse_args(args):
    def int_positive(string):
        ivalue = int(string)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f'{string} is not positive')
        return ivalue

    parser = argparse.ArgumentParser(description='Cloudfalre prometheus exporter')
    parser.add_argument('-t', '--token', type=str, required=True,
                        help='Cloudflare API Token')
    parser.add_argument('--host', type=str,
                        help='TCP/IP host for HTTP server',
                        default=DEFAULT_HOST)
    parser.add_argument('--port', type=int_positive,
                        help="Port used to expose metrics for Prometheus",
                        default=DEFAULT_PORT)
    parser.add_argument('--logs_fetch', type=bool,
                        help="Activate metric from logs",
                        default=DEFAULT_LOGS_FETCH)
    parser.add_argument('--logs_count', type=int_positive,
                        help="Cloudflare logs: count param",
                        default=DEFAULT_LOGS_COUNT)
    parser.add_argument('--logs_sample', type=int_positive,
                        help="Cloudflare logs: sample param [0-1]",
                        default=DEFAULT_LOGS_SAMPLE)
    parser.add_argument('--logs_range', type=int_positive,
                        help="Cloudflare logs: range in seconds",
                        default=DEFAULT_LOGS_RANGE)
    return parser.parse_args(args)


def main():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    args = parse_args(sys.argv[1:])
    REGISTRY.register(CloudflareCollector(cloudflare_token=args.token,
                                          logs_fetch=args.logs_fetch,
                                          logs_count=args.logs_count,
                                          logs_sample=args.logs_sample,
                                          logs_range=args.logs_range))
    app = web.Application()
    app.router.add_get('/metrics', handle_metrics)
    app.router.add_get('/health', handle_health)
    print(f'======== Running on http://{args.host}:{args.port}/metrics ========')
    web.run_app(app, host=args.host, port=args.port, access_log=None,
                print=False)


if __name__ == '__main__':
    main()
