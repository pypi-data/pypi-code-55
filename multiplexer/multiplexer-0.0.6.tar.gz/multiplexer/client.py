from random import SystemRandom
from bitstring import Bits, BitStream

rnd = SystemRandom()


class Plex():
    def __init__(self, book):
        self.book = Bits(hex=book)
        self.len = self.book.len
        self._check_book()

    def _check_book(self):
        if self.len / 8 < 500000:
            raise Exception('Less than 500K bytes in the book')

    def encode(self, text):
        bits = Bits(bytes=text.encode('utf-8'))
        stream = BitStream(bits)
        out = list()

        while stream.bitpos != stream.len:
            match = self.book.rfind(
                stream.peek(8),
                start=rnd.randint(0, self.len),
                bytealigned=True
            )
            while not match:
                match = self.book.rfind(
                    stream.peek(8),
                    start=rnd.randint(0, self.len),
                    bytealigned=True
                )
            stream.pos += 8
            out.append(match[0])
            text = text[2:]
        return out

    def decode(self, array):
        out = ''
        bs = BitStream(self.book)
        for val in array:
            bs.pos = val
            out += bs.read(8).hex
        return Bits(hex=out).tobytes().decode()
