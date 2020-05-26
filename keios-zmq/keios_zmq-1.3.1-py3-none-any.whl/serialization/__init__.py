import io
import struct


class DataInputStream:
    """
    Poor copy of the java datainputstream
    """

    def __init__(self, stream: io.BytesIO):
        self.stream: io.BytesIO = stream

    def read_byte(self):
        return struct.unpack('b', self.stream.read(1))[0]

    def read_int(self) -> int:
        return struct.unpack('>i', self.stream.read(4))[0]

    def read_utf(self) -> str:
        utf_length = struct.unpack('>h', self.stream.read(2))[0]
        return self.stream.read(utf_length).decode("utf-8")

    def read_bytes(self) -> bytes:
        """
        :return: remaining bytes from the stream
        """
        return self.stream.read()

    def close(self):
        return self.stream.close()


class DataOutputStream:
    def __init__(self, stream: io.BytesIO):
        self.stream = stream

    def write_bytes(self, b: bytes) -> int:
        return self.stream.write(b)

    def write_int(self, i: int) -> int:
        return self.stream.write(int.to_bytes(i, 4, 'big'))

    def write_utf(self, s: str) -> int:
        self.stream.write(struct.pack('>h', len(s)))
        return self.stream.write(s.encode("utf-8"))

    def to_bytes(self) -> bytes:
        return self.stream.getvalue()

    def close(self):
        return self.stream.close()