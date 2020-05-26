from abc import ABC, abstractmethod
from typing import List

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.log_provider import LogProvider


class KeiosMessageHandler(ABC):
    log = LogProvider.get_logger(__name__)

    @abstractmethod
    def handle(self, messages: List[KeiosMessage]):
        pass

    def execute(self, messages: List[KeiosMessage]):
        if self.is_healthcheck_message(messages[0]):
            return self.build_healthcheck_response()
        else:
            return self.handle(messages)

    def is_healthcheck_message(self, message: KeiosMessage):
        if message.header.get("type") == "HCheck":
            return True
        else:
            return False

    def build_healthcheck_response(self) -> List[KeiosMessage]:
        return [KeiosMessage({'type': 'HCheck'}, bytes("pong", encoding="utf-8"))]
