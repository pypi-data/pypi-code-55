# -*- coding: utf-8 -*-
import struct
import math

# The ZMQ frames from the audio encoder are expected
# to have the following format, in pseudo C struct, no alignment,
# little-endian. See ODR-DabMux' src/input/Zmq.h for reference.
#
#   uint16_t version; // we support version=1 now
#   uint16_t encoder; // see ZMQ_ENCODER_XYZ
#
#   /* length of the 'data' field */
#   uint32_t datasize;
#
#   /* Audio level, peak, linear PCM */
#   int16_t audiolevel_left;
#   int16_t audiolevel_right;
#
#   /* Data follows the header */
#   uint8_t data[datasize];

class ZMQFrameDecoder:
    """
    Decode a frame and extract the header information
    """

    def __init__(self, frame):
        frame_header = "<HHIhh"

        headersize = struct.calcsize(frame_header)
        if len(frame) > headersize:
            # > instead of >= because we want to ensure there's also payload
            unpacked = struct.unpack(frame_header, frame[:headersize])
            self.version, self.encoder, datasize, self.audiolevel_left, self.audiolevel_right = unpacked

            if len(frame) == headersize + datasize:
                self.data = frame[headersize:]
            else:
                self.data = None
        else:
            self.version = self.encoder = self.audiolevel_left = self.audiolevel_right = None
            self.data = None

    def is_valid(self):
        return self.version_is_valid() and self.data is not None

    def version_is_valid(self):
        # See ODR-DabMux' src/input/Zmq.cpp for reference
        return self.version == 1

    def get_audio_levels(self):
        """
        Returns a tuple with left and right audio levels, or (None, None) if frame is not valid
        """
        if not self.version_is_valid():
            return (None, None)
        else:
            int16_max = 0x7FFF
            try:
                dB_l = round(20*math.log10(float(self.audiolevel_left) / int16_max), 1)
            except ValueError:
                dB_l = -90.0

            try:
                dB_r = round(20*math.log10(float(self.audiolevel_right) / int16_max), 1)
            except ValueError:
                dB_r = -90.0

            return (dB_l, dB_r)


