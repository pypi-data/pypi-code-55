import json
import sys
from wsgiref.simple_server import make_server

from . import NAME, VERSION, Kaa, KaaServer
from .openapi import OpenApi
from .server import Server


class Cli():

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8086
        self.argv = sys.argv[:]

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'

        if subcommand == 'version':
            msg = self.__get_version
        elif subcommand == 'help':
            msg = self.__get_help()
        elif subcommand == 'serve':
            self.__serve()
            return
        elif subcommand == 'openapi':
            server:KaaServer = Server().get_server()
            kaa:Kaa = server.get_kaa({
                'REQUEST_METHOD': '',
                'PATH_INFO': '',
                'REMOTE_ADDR': '',
                'QUERY_STRING': ''
            }, None)

            msg = json.dumps(OpenApi().generate(kaa))
        else:
            msg = 'Invalid command. Try help'

        sys.stdout.write(msg + '\n')

    def __get_name(self):
        return NAME

    def __get_version(self):
        return VERSION

    def __get_help(self):
        commands = [
            ('version', 'Returns Kaa version'),
            ('serve', 'Starts a server for development'),
            ('openapi', 'Generates openapi json')
        ]
        return '\n'.join(['{}\t\t{}'.format(*cmd) for cmd in commands])

    def __serve(self):
        self.__set_host_port()
        sys.stdout.write('{} version {}\n'.format(self.__get_name(), self.__get_version()))
        sys.stdout.write('Server started at {}:{}\n\n'.format(self.host, self.port))
        server:KaaServer = Server().get_server()
        make_server(
            host=self.host,
            port=int(self.port),
            app=lambda env, start_response: server.get_kaa(env, start_response).serve()
        ).serve_forever()

    def __set_host_port(self):
        try:
            porthost = self.argv[2].split(':')
            if len(porthost) == 1:
                self.port = porthost[0]
            elif len(porthost) == 2:
                self.host = porthost[0]
                self.port = porthost[1]
            else:
                sys.stdout.write('Invalid host:port' + '\n')
                sys.exit(1)
        except IndexError:
            pass
