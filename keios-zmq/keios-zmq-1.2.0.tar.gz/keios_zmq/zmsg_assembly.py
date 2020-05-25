import io
from typing import List

from keios_zmq.keios_message import KeiosMessage
from keios_zmq.serialization import DataInputStream, DataOutputStream


class ZMsgAssembly:
    """
    Serializes / Deserializes KeiosMessages from the given ZMQMessage (which isn
    """

    @staticmethod
    def assemble(messages: List[KeiosMessage]) -> List[bytes]:
        if len(messages) == 0:
            return [bytes(0xF)]
        l = []
        for msg in messages:
            stream = io.BytesIO()
            dos = DataOutputStream(stream)
            dos.write_int(len(msg.header))
            for k, v in msg.header.items():
                dos.write_utf(f'{k}:{v}')
                dos.write_bytes(bytes([0x00]))
            dos.write_bytes(msg.payload)
            l.append(dos.to_bytes())
            dos.close()
        return l

    @staticmethod
    def disassemble(zmsg: List[bytes]) -> List[KeiosMessage]:
        l = []
        for msg in zmsg:
            if msg == bytes(0xF): #empty response denoted by 0xF
                return []
            stream = io.BytesIO(msg)
            dis = DataInputStream(stream)
            header_length = dis.read_int()

            header = {}
            for _ in range(0, header_length):
                k, v = dis.read_utf().split(':')
                dis.read_byte()
                header[k] = v
            payload = dis.read_bytes()
            l.append(KeiosMessage(header, payload))
            stream.close()

        return l
