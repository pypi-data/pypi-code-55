# -*- coding: utf-8 -*-

import time
from .afpacket import AFEncoder

class EDIFrameEncoder:
    def __init__(self):
        self._dflc = 0
        self._seq = 0
        self._start_time = time.clock_gettime(time.CLOCK_MONOTONIC)
        self._last_time_odra = self._start_time

    def encode_edi_frame(self, payload, audiolevels, version):
        afencoder = AFEncoder()
        major = 0
        minor = 0
        afencoder.add_starptr(b'DSTI', major, minor)

        tsta = 0xFFFFFF # disable tsta, utco, seconods
        utco = 0
        seconds = 0

        afencoder.add_dsti(self._dflc, tsta, utco, seconds)
        self._dflc += 1

        stream_id = 1
        afencoder.add_ssm(stream_id, payload)

        audio_left, audio_right = audiolevels
        afencoder.add_odr_audio(audio_left, audio_right)

        time_now = time.clock_gettime(time.CLOCK_MONOTONIC)
        if self._last_time_odra + 10 < time_now: # to save bandwidth
            self._last_time_odra += 10

            uptime = int(time_now - self._start_time)
            afencoder.add_odr_version(uptime, version.encode())

        tagpacket_alignment = 0
        packet = afencoder.build_afpacket(self._seq, tagpacket_alignment)
        self._seq += 1
        return packet
