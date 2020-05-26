# -*- coding: utf-8 -*-
import time
import logging
import zmq
import socket
from io import BytesIO

from .frame import ZMQFrameDecoder
from .edi.decoder import EDIFrameDecoder, DecodeError

logger = logging.getLogger(__name__)

class InputFrame:
    """An inputframe contains 120ms of data, i.e. one DAB+ superframe.

    That's the easiest way to guarantee proper alignment"""
    PROTO_ZMQ = "zmq"
    PROTO_EDI = "edi"

    # TODO handle source uptime

    def __init__(self, protocol, port, audiolevels, data, zmqinfo=None, ediinfo=None):
        self.protocol = protocol
        self.port = port

        # The idea is to re-use the same source data when doing EDI->EDI and ZMQ->ZMQ, and
        # regenerate the output frame from the decoded fields when switching protocols.
        self.zmqinfo = zmqinfo # contains { 'version': <int>, 'encoder': <int>, 'rawframe': <bytes> } or None
        self.ediinfo = ediinfo # contains { 'encoder': <bytes>, 'uptime': <int>, 'rawframes': [<bytes>] } or None

        # audiolevels in dB
        self.audiolevel_left, self.audiolevel_right = audiolevels
        self.data = data

class InputBase:
    def __init__(self, delay_settings):
        self.delay_settings = delay_settings
        time_now = time.time()
        self._last_beat = time_now - float(self.delay_settings.nodata_failover_delay)
        self._last_audio_ok = time_now - float(self.delay_settings.noaudio_failover_delay)
        self._inhibit_switching_until = time_now
        self._audio_left, self._audio_right = (None, None)

    def tick(self):
        time_now = time.time()

        if self._last_beat + self.delay_settings.nodata_failover_delay < time_now:
            inh_switch_until = time_now + self.delay_settings.nodata_recover_delay

            if inh_switch_until > self._inhibit_switching_until:
                logger.debug("Input {} inhibit until {} because nodata".format(
                    self.port,
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inh_switch_until))))

            self._inhibit_switching_until = max(self._inhibit_switching_until, inh_switch_until)

        if self._last_audio_ok + self.delay_settings.noaudio_failover_delay < time_now:
            inh_switch_until = time_now + self.delay_settings.noaudio_recover_delay

            if inh_switch_until > self._inhibit_switching_until:
                logger.debug("Input {} inhibit until {} because noaudio".format(
                    self.port,
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(inh_switch_until))))

            self._inhibit_switching_until = max(self._inhibit_switching_until, inh_switch_until)

    def _update_state(self, frame):
        time_now = time.time()

        if frame.is_valid():
            self._last_beat = time_now

        self._audio_left, self._audio_right = frame.get_audio_levels()

        if self.delay_settings.audio_threshold != -90:
            has_valid_audio = (self._audio_left is not None) and \
                              (self._audio_right is not None) and \
                              (self._audio_left > self.delay_settings.audio_threshold) and \
                              (self._audio_right > self.delay_settings.audio_threshold)
            if has_valid_audio:
                self._last_audio_ok = time_now
        else:
            # Assume audio is always ok
            self._last_audio_ok = time_now

    def is_available(self):
        """
        check if the input instance is 'available':
        "last time ticked less than failover duration"
        """
        time_now = time.time()
        has_recently_received_data = self._last_beat > (time_now - float(self.delay_settings.nodata_failover_delay))
        has_valid_audio = self._last_audio_ok > (time_now - float(self.delay_settings.noaudio_failover_delay))
        is_not_inhibited = self._inhibit_switching_until < time_now

        return has_recently_received_data and has_valid_audio and is_not_inhibited

    def last_beat(self):
        return self._last_beat

    def last_audio_ok(self):
        return self._last_audio_ok

    def get_audio_levels(self):
        return (self._audio_left, self._audio_right)

class EDIInput(InputBase):
    """The EDI input handles connection/disconnection, and only
    handles a single connection.

    If disconnected, get_socket() will return the listener socket, and if
    that polls a POLLIN event, accept() can be called.

    This will connect the input, and get_socket() will return the connected socket.
    Once that polls a POLLIN event, recv() can be used to retreive data"""

    def __init__(self, port, delay_settings):
        super(EDIInput, self).__init__(delay_settings)
        self.protocol = "edi"
        self.port = port
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.setblocking(False)
        s.listen(1)
        self._listen_sock = s
        self._sock = None
        self._remote_addr = None
        self._decoder = EDIFrameDecoder()

        self._reinit()

    def _reinit(self):
        self._num_frames_collected = 0
        self._last_dflc = None
        self._buf = bytearray()
        self._rawframes = []

    def __str__(self):
        if self.is_connected():
            return '<EDIInput: port {} connected to {}'.format(self.port, self._remote_addr)
        else:
            return '<EDIInput: listening port {}>'.format(self.port)

    def is_connected(self):
        return self._sock is not None

    def get_socket(self):
        #This returns the fileno of the socket, because that's also what poll needs
        return self._sock.fileno() if self.is_connected() else self._listen_sock.fileno()

    def stop(self):
        logger.debug('Stopping listener on port {}'.format(self.port))
        if self._sock:
            self._close_conn()
        self._listen_sock.close()

    def _close_conn(self):
        logger.info('Close {} -> {}'.format(self.port, self._remote_addr))
        if self._sock:
            self._sock.close()
        self._sock = None
        self._remote_addr = None

    def recv(self):
        """Handle both accepting new connections and receiving data.

        Returns None when no frame available (which doesn't imply no data was received from
        the socket) or an InputFrame.
        """
        if self._sock is None:
            self._sock, self._remote_addr = self._listen_sock.accept()
            self._sock.setblocking(False)
            return None

        dat = self._sock.recv(512)
        if dat == b'':
            self._close_conn()
        else:
            self._decoder.load_data(dat)
            while True:
                try:
                    af = self._decoder.get_afpacket()
                    if af is None:
                        break
                    (rawframe, af_packet) = af
                    # Not only must we check for consecutive frames, but we must also ensure
                    # the first frame counter is zero modulo 5 (DAB+ superframe alignment), because
                    # if we receive over EDI and send over ZMQ we have to align those
                    if (self._last_dflc is None and (af_packet.dflc % 5) == 0) or self._last_dflc + 1 == af_packet.dflc:
                        self._last_dflc = af_packet.dflc
                        self._buf.extend(af_packet.istd)
                        self._rawframes.append(rawframe)
                        self._num_frames_collected += 1

                        if self._num_frames_collected == 5:
                            self._update_state(af_packet)
                            ediinfo = {
                                    'version': af_packet.version,
                                    'uptime': af_packet.uptime,
                                    'rawframes': self._rawframes}
                            al = (af_packet.audio_left, af_packet.audio_right)
                            f = InputFrame(InputFrame.PROTO_EDI, self.port, al, self._buf, ediinfo=ediinfo)
                            self._reinit()
                            return f
                    else:
                        self._reinit()
                except DecodeError:
                    logging.error("Closing EDI connection to {} because of decode error".format(self.port))
                    self._close_conn()
                    return None
        return None

class StreamInput(InputBase):
    """
    Input wrapper for ZMQ inputs
    """
    def __init__(self, zmq_ctx, port, delay_settings, tcp_accepted_ret=None):
        """
        audio threshold is in range [-90..0] dB
        """
        super(StreamInput, self).__init__(delay_settings)
        self.port = port
        self.protocol = "zmq"

        self.zmq_ctx = zmq_ctx
        s = self.zmq_ctx.socket(zmq.SUB)
        s.bind('tcp://*:{port}'.format(port=self.port))
        s.setsockopt(zmq.SUBSCRIBE, b"")
        self._sock = s

    def __str__(self):
        return '<StreamInput: ZMQ port {}>'.format(self.port)

    def get_socket(self):
        """Return the socket, which can be either a zmq or a native socket"""
        return self._sock

    def stop(self):
        logger.debug('Stopping socket on port {}'.format(self.port))
        # close zmq and edi socket
        self._sock.close()

    def recv(self):
        """
        Ask for receiving a message.

        Returns None if no message received, or an InputFrame
        """

        try:
            msg = self._sock.recv(zmq.NOBLOCK)
            frame = ZMQFrameDecoder(msg)
            self._update_state(frame)
            if frame.is_valid():
                zmqinfo = { 'version': frame.version, 'encoder': frame.encoder, 'rawframe': msg }
                al = (frame.audiolevel_left, frame.audiolevel_right)
                return InputFrame(InputFrame.PROTO_ZMQ, self.port, al, frame.data, zmqinfo=zmqinfo)
        except zmq.ZMQError as e:
            if e.errno != zmq.EAGAIN:
                logger.warn("ZMQ recv from port {} error: {}".format(self.port, e))
                raise
            return None

