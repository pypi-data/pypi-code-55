from .error import Error, RequestError, IdentifierError
from .sites import Sites


class Client(object):
    def __init__(self):
        self.api_key = None
        self.sites = Sites(self)

    def set_api_key(self, api_key):
        self.api_key = api_key
