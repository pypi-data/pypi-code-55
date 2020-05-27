#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM
from wsgiref.simple_server import WSGIRequestHandler
# from werkzeug.serving import WSGIRequestHandler
from logging import error, exception
from time import sleep

class Handler(WSGIRequestHandler):
    protocol_version = "HTTP/1.1"

class Server:
    ssl_context = None
    multithread = False
    multiprocess = False
    server_address = 'localhost'
    passthrough_errors = False
    shutdown_signal = False

    def __init__(self, addr, app):
        (host, port) = self.addr = addr
        # Set up base environment
        env = self.base_environ = {}
        env['SERVER_NAME'] = host
        env['GATEWAY_INTERFACE'] = 'HTTP/1.1'
        env['SERVER_PORT'] = port
        env['REMOTE_HOST']=''
        env['CONTENT_LENGTH']=''
        env['SCRIPT_NAME'] = ''

        self.app = app

    def run(self):
        import os
        while True:
            with socket(AF_INET, SOCK_STREAM) as s:
                try:
                    s.connect(self.addr)
                except Exception as e:
                    error("Connect: %s", e)
                    sleep(2)
                    continue
                print("Handling in", os.getpid())

                try:
                    Handler(s, self.addr, server)
                except Exception as e:
                    exception("WSGIRequestHandler")
                    sleep(1)
                    continue

    def get_app(self):
        return self.app

if __name__ == "__main__":
    from argparse import ArgumentParser
    from asyncio import get_child_watcher, get_event_loop
    from importlib import import_module
    from multiprocessing import Process
    from sys import path

    path.insert(0, ".")

    def address(str):
        (host, port) = str.rsplit(":", 1)
        return (host, int(port))

    def func(str):
        (module, symbol) = str.rsplit(":", 1)
        module = import_module(module)
        return getattr(module, symbol)

    parser = ArgumentParser(description="Run WSGI app in sequential `worker` mode")
    parser.add_argument("--connect", default="localhost:4040", type=address,
        help="Load Balancer Hub to connect to [host:port]")
    parser.add_argument("--workers", default=1, type=int,
        help="Number of worker Processes")
    parser.add_argument("app", nargs='?', default="wsgiref.simple_server:demo_app", type=func,
        help="The WSGI request handler to handle requests")
    args = parser.parse_args()

    loop = get_event_loop()
    server = Server(args.connect, args.app)
    watcher = get_child_watcher()
    watcher.attach_loop(loop)

    def launch():
        p = Process(target=server.run)
        p.start()
        watcher.add_child_handler(p.pid, lambda a, b: launch())

    async def setup():
        for _ in range(args.workers):
            launch()

    loop.run_until_complete(setup())
    loop.run_forever()
