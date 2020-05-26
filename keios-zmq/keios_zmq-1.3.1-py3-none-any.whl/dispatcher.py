from typing import Callable, List

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.keios_message_handler import KeiosMessageHandler
from keios_zmq.log_provider import LogProvider


class Dispatcher(KeiosMessageHandler):
    log = LogProvider.get_logger(__name__)

    def __init__(self,
                 message_handler: Callable[[List[KeiosMessage]], List[KeiosMessage]],
                 error_handler: Callable[[Exception], List[KeiosMessage]] = None):
        self._message_handler = message_handler
        self._error_handler = error_handler

    def handle(self, messages: List[KeiosMessage]):
        try:
            return self._message_handler(messages)
        except Exception as e:
            self.log.error("Unhandled exception occurred:", exc_info=e)
            if self._error_handler is not None:
                return self._error_handler(e)
            else:
                self.log.error("No error handler has been set. ignoring and returning empty list:", exc_info=e)
                return []
