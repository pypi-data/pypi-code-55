import logging

from . import Client, HttpAuth

logger = logging.getLogger('rbx.clients.panels')


class PanelsClient(Client):
    """API Client for the Panels Service."""
    def __init__(self, endpoint, token):
        super().__init__()
        self.ENDPOINT = endpoint.rstrip('/')
        self.token = token

    @property
    def auth(self):
        """The Panels Service uses Digest Authentication."""
        return HttpAuth(self.token, key='X-RBX-TOKEN')

    def search(self, **parameters):
        """Perform a Panels search."""
        return self._post('/search', data=parameters)
