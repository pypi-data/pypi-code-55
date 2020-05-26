from typing import Callable, List, Generator

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.keios_message_handler import KeiosMessageHandler
from keios_zmq.log_provider import LogProvider


class StreamingDispatcher(KeiosMessageHandler):
    log = LogProvider.get_logger(__name__)

    def __init__(self,
                 message_handler: Callable[[List[KeiosMessage]], Generator[KeiosMessage, None, None]],
                 error_handler: Callable[[Exception], Generator[KeiosMessage, None, None]] = None):
        self._message_handler = message_handler
        self._error_handler = error_handler

    def handle(self, messages: List[KeiosMessage]):
        return self._message_handler(messages)
