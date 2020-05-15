import asyncio
from typing import Optional, Callable
from inspect import isclass, signature
from functools import partial

import websockets

from soc.request import Request
from soc.socket_view import SocketView

import logging

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s %(message)s")


class Soc(object):

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None):
        self.host: str = host or "localhost"
        self.port: int = port or 8765
        self.logger = logging.getLogger()
        self.view_functions: dict = {}
        self.error_handlers: dict = {}

    def route(self, path: str):
        """ Route decorator """

        def decorator(f):
            self.add_route(path, f)
            return f
        return decorator

    def add_route(self, path: str, func: Callable) -> None:
        """ Add a route """

        if isclass(func) and issubclass(func, SocketView):
            sig = signature(func.handler)
        else:
            sig = signature(func)

        # Check to ensure any handlers include a param for the request
        if not len(sig.parameters):
            raise ValueError("Handlers must include at least 1 parameter for the request")

        if path in self.view_functions.keys():
            raise ValueError(f"path {path} already exists")

        self.view_functions.update({path: func})

    def add_error_handler(self, exception, handler: Callable) -> None:
        """ Add an exception handler """

        if not issubclass(exception, Exception):
            raise TypeError(f"exception must be an Exception or subclass of Exception")
        if not callable(handler):
            raise TypeError("handler must be callable")

        self.error_handlers.update({exception: handler})

    async def main(self, websocket, path: str):
        """ Main request handler """

        data: str = await websocket.recv()
        self.logger.info(path)

        request: Request = Request(websocket=websocket, full_path=path, data=data)

        if path in self.view_functions:
            # Get URL params from URL
            view_func = self.view_functions[path]

            # If view_func is subclassed from SocketView
            if isclass(view_func) and issubclass(view_func, SocketView):
                # Create an instance and call the handler method
                instance = view_func()
                callable_view_func: Callable = partial(instance.handler, request)
            else:
                callable_view_func: Callable = partial(view_func, request)
            try:
                await websocket.send(callable_view_func())
            except Exception as e:
                if e in self.error_handlers.keys():
                    await websocket.send(self.error_handlers[e](e))
                await websocket.send('{"error": "Application error"}')
        else:
            await websocket.send('{"error": "Not found"}')

    def run(self, host: Optional[str] = None, port: Optional[int] = None):
        """ Start the server """
        self.logger.info(f"Starting socker server on {host or self.host}:{port or self.port}")
        start_server = websockets.serve(self.main, host or self.host, port or self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
