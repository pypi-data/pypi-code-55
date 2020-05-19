
import logging
import websockets


class WSocket:
    def __init__(self, uri, debug=False):
        """
        """
        self.uri = uri

        if debug:
            logger = logging.getLogger('websockets')
            logger.setLevel(logging.DEBUG)
            logger.addHandler(logging.StreamHandler())

    async def __aenter__(self):
        """
        """
        self._conn = websockets.connect(self.uri, subprotocols=['graphql-ws'])
        self.websocket = await self._conn.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        """
        """
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        """
        """
        await self.websocket.send(message)

    async def receive(self):
        """
        """
        return await self.websocket.recv()
