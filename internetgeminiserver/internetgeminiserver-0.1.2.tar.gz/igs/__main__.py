import asyncio
import os
import pathlib
import ssl
import subprocess
import tempfile
import urllib.parse
import argparse
import configparser
import mimetypes
from datetime import datetime

SUCCESS = 20
NOT_FOUND = 51
PROXY_REQUEST_REFUSED = 53
BAD_REQUEST = 59

config = None
server_port = None


class GeminiProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.remote = None
        self.header_buffer = b''

    def access_log(self, domain, status, path, mime):
        if not config.has_section(domain):
            return

        if not config.has_option(domain, 'access_log'):
            return

        stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log = config.get(domain, 'access_log')
        with open(log, 'a') as handle:
            handle.write(f'{domain} {self.remote} [{stamp}] "{path}" {status} {mime}\n')

    def error_log(self, domain, status, path, error):
        if not config.has_section(domain):
            return

        if not config.has_option(domain, 'error_log'):
            return

        stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.access_log(domain, status, path, '-')
        log = config.get(domain, 'error_log')
        with open(log, 'a') as handle:
            handle.write(f'{domain} {self.remote} [{stamp}] "{path}" {status} {error}\n')

    def connection_made(self, transport):
        self.transport = transport
        self.remote = transport.get_extra_info('peername')[0]

    def data_received(self, data: bytes):
        self.header_buffer += data
        if len(self.header_buffer) > 1024:
            self.make_response(BAD_REQUEST, "Header too large")
            self.transport.close()

        if b'\r\n' in self.header_buffer:
            header, body = self.header_buffer.split(b'\r\n', 1)
            try:
                header = header.decode().strip()
            except:
                self.make_response(BAD_REQUEST, "Could not decode header")
                self.transport.close()
                return

            try:
                url = urllib.parse.urlparse(header, scheme='gemini')
            except:
                self.make_response(BAD_REQUEST, "Could not parse url")
                self.transport.close()
                return

            if url.scheme != "gemini":
                self.error_log(url.netloc, PROXY_REQUEST_REFUSED, url.path,
                               f"Proxy refused, requested protocol {url.scheme}")
                self.make_response(PROXY_REQUEST_REFUSED, "Proxy refused")
                self.transport.close()
                return

            self.handle_request(url)
            self.transport.close()

    def make_response(self, status, meta):
        response = f'{status}  {meta}\r\n'
        self.transport.write(response.encode('utf-8'))

    def handle_request(self, url):
        hostname = url.netloc

        if ':' in hostname:
            hostname, port = hostname.split(':')

        path = url.path
        if not config.has_section(hostname):
            self.error_log(hostname, BAD_REQUEST, path, "domain unknown")
            self.make_response(BAD_REQUEST, "Domain not found")
            self.transport.close()
            return

        root = config.get(hostname, 'root')
        client_path = path
        path = os.path.normpath(path).strip('/')
        full_path = os.path.abspath(os.path.join(root, path))
        if os.path.isfile(full_path):
            self.respond_file(path, hostname, client_path)
            return

        for suffix in ['index.gmi', 'index.gemini']:
            index = os.path.join(full_path, suffix)
            if os.path.isfile(index):
                self.respond_file(index, hostname, client_path)
                return

        self.make_response(NOT_FOUND, "Not found")
        self.transport.close()
        self.error_log(hostname, NOT_FOUND, client_path, "not found")

    def respond_file(self, path, hostname, log_path):
        mime, encoding = mimetypes.guess_type(path)
        if mime is None:
            mime = "application/octet-stream"
        self.make_response(SUCCESS, mime)

        self.access_log(hostname, SUCCESS, log_path, mime)

        if mime.startswith('text/'):
            with open(path, 'r', newline=None) as handle:
                data = handle.read().replace('\n', '\r\n').encode('utf-8')
        else:
            with open(path, 'rb') as handle:
                data = handle.read()
        self.transport.write(data)
        self.transport.close()


async def run_main(host, port, ssl=None):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(GeminiProtocol, host, port, ssl=ssl)
    await server.serve_forever()


def generate_test_cert():
    hostname = 'localhost'
    certfile = pathlib.Path(tempfile.gettempdir()) / f"{hostname}.crt"
    keyfile = pathlib.Path(tempfile.gettempdir()) / f"{hostname}.key"
    if not certfile.exists() or not keyfile.exists():
        print(f"Writing ad hoc TLS certificate to {certfile}")
        subprocess.run(
            [
                f"openssl req -newkey rsa:2048 -nodes -keyout {keyfile}"
                f' -nodes -x509 -out {certfile} -subj "/CN={hostname}"'
            ],
            shell=True,
            check=True,
        )
    return str(certfile), str(keyfile)


def make_ssl_context():
    certfile, keyfile = generate_test_cert()

    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_OPTIONAL
    context.load_cert_chain(certfile, keyfile)

    context.load_default_certs(purpose=ssl.Purpose.CLIENT_AUTH)

    return context


def main():
    global config
    parser = argparse.ArgumentParser(description="International Gemini Station")
    parser.add_argument('config', help='Config file location')
    parser.add_argument('--host', help='Bind to address (default: 127.0.0.1)', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='Bind to port (default: 1965)', default=1965, type=int)
    parser.add_argument('-s', '--ssl', help='Generate test ssl cert (default: off)', action='store_true')
    args = parser.parse_args()

    if args.ssl:
        print("Starting with a self-signed ssl cert")
        ssl = make_ssl_context()
    else:
        print("Starting without ssl, run a loadbalancer in front of this")
        ssl = None

    if not os.path.isfile(args.config):
        print("Config file not found")
        exit(1)

    config = configparser.ConfigParser()
    config.read(args.config)

    mimetypes.init()
    mimetypes.add_type('text/gemini', '.gemini')
    mimetypes.add_type('text/gemini', '.gmi')
    asyncio.run(run_main(args.host, args.port, ssl=ssl))


if __name__ == '__main__':
    main()
