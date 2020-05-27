from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.zmsg_assembly import ZMsgAssembly


@dataclass
class BulkMessage:
    identifier: bytes
    messages: List[KeiosMessage]


class ZMQServer(ABC):
    """
    server interface
    """

    @abstractmethod
    def start_server(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def destruct(self, zmsg: List) -> List:
        return [zmsg[0], ZMsgAssembly.disassemble(zmsg[1:])]

    def construct(self, identitfier: bytes, messages: List[KeiosMessage]) -> List[bytes]:
        return [identitfier] + ZMsgAssembly.assemble(messages)
