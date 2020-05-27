
# TODO: 支持RPC通信

from .session import BaseDownloadSession
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from urllib.parse import urlparse


class RPCDownloadClient:
    pass


class RPCDownloadServer(BaseDownloadSession):
    def __init__(self, address, port):
        self._address = address
        urlparse(address)
        SimpleXMLRPCServer(('localhost', ))
        pass

