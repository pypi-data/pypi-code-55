# -*- coding: utf-8 -*-
import logging
import struct

from .crc16 import crc16
from .afpacket import AFDecoder, NeedMoreData

logger = logging.getLogger(__name__)

class DecodeError(BaseException):
    pass

class EDIFrameDecoder:
    """
    Receives incoming bytes from the TCP stream and assembles them
    into EDI frames
    """
    def __init__(self):
        self._buf = bytearray()

    def load_data(self, data):
        self._buf.extend(data)

    def get_afpacket(self):
        """
        Returns an AFDecoder on successful decode, or None
        """
        if len(self._buf) < 2:
            return None

        if self._buf[:2] != b'AF':
            raise DecodeError()

        try:
            afdecoder = AFDecoder()
            (decode_success, bytes_consumed) = afdecoder.decode_af(self._buf)

            if decode_success:
                rawframe = self._buf[:bytes_consumed]
                self._buf = self._buf[bytes_consumed:]
                return (rawframe, afdecoder)

        except NeedMoreData:
            pass
        return None

