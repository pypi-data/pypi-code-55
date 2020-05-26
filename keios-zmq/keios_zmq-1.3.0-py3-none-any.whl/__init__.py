import time
from logging import Logger
from typing import Callable, List, Generator

from keios_zmq.asyncio_zmq_server import AsyncioKeiosZMQ
from keios_zmq.blocking_zmq_server import KeiosZMQ
from keios_zmq.keios_message import KeiosMessage
from keios_zmq.log_provider import LogProvider
from keios_zmq.dispatcher import Dispatcher
from keios_zmq.pool_zmq_server import PoolKeiosZMQ
from keios_zmq.streaming_asyncio_zmq_server import StreamingAsyncioZmqServer
from keios_zmq.streaming_dispatcher import StreamingDispatcher
from keios_zmq.zmq_server import ZMQServer


class KeiosZMQFactory:
    @staticmethod
    def get_server(name: str,
                   message_handler: Callable[[List[KeiosMessage]], List[KeiosMessage]],
                   error_handler: Callable[[Exception], List[KeiosMessage]] = None,
                   port=8077) -> ZMQServer:
        """
        :param name:
        :param message_handler: handles the serialized message and returns a serialized message which will be sent as response
        :param error_handler: receives the unhandled exception and return a serialized response (an error)
        :param port:
        :return: a keios zmq server depending on the given name. Defaults to blocking keios zmq server
        """
        log: Logger = LogProvider.get_logger(__name__)
        dispatcher = Dispatcher(message_handler, error_handler)
        if name == "blocking":
            return KeiosZMQ(port, dispatcher)
        if name == "pool":
            return PoolKeiosZMQ(port, dispatcher)
        if name == "asyncio":
            return AsyncioKeiosZMQ(port, dispatcher)
        log.warning(f"'{name}' is not a valid KeiosZMQ server implementation. Using blocking.")
        return KeiosZMQ(port, dispatcher)

    @staticmethod
    def get_streaming_server(message_handler: Callable[[List[KeiosMessage]], Generator[KeiosMessage, None, None]], port=8077):
        return StreamingAsyncioZmqServer(port, StreamingDispatcher(message_handler))