# -*- coding: utf-8 -*-
import logging
import struct
import socket
import threading
import zmq
from zmq.utils.monitor import recv_monitor_message
from .edi.encoder import EDIFrameEncoder

logger = logging.getLogger(__name__)

class ZMQOutput:
    """
    Output instance. Connects to remote socket and relays the ZMQ frames.

    Uses zmq-socket-monitor to see if we are connected to the subscriber.
    """
    def __init__(self, zmq_ctx, output):
        self.zmq_ctx = zmq_ctx
        self.protocol = "zmq"
        self.output = output
        self._out_endpoint = output['endpoint']
        logger.debug('Connecting output to {}'.format(self._out_endpoint))
        self.connection = self.zmq_ctx.socket(zmq.PUB)
        self._monitor_thread = threading.Thread(target=ZMQOutput._monitor, args=(self,))
        self._monitor_thread.start()
        self.connection.connect(self._out_endpoint)
        self.connected = True

        self._num_subscribers_lock = threading.Lock()
        self._num_subscribers = 0

    def _monitor(self):
        try:
            monitor = self.connection.get_monitor_socket()
            while monitor.poll():
                evt = recv_monitor_message(monitor)
                if evt['event'] == zmq.EVENT_CONNECTED:
                    self._num_subscribers_lock.acquire()
                    self._num_subscribers += 1
                    self._num_subscribers_lock.release()
                elif evt['event'] == zmq.EVENT_DISCONNECTED:
                    self._num_subscribers_lock.acquire()
                    self._num_subscribers -= 1
                    self._num_subscribers_lock.release()
                elif evt['event'] == zmq.EVENT_MONITOR_STOPPED:
                    break
            monitor.close()

        except zmq.ZMQError as e:
            # TODO: how to handle this case? what did went wrong?
            logger.error('Unable to initialize monitor - {}'.format(e))

    def is_connected(self):
        self._num_subscribers_lock.acquire()
        num_sub = self._num_subscribers
        self._num_subscribers_lock.release()
        return num_sub > 0

    def stop(self):
        logger.debug('Stopping output to {}'.format(self._out_endpoint))
        try:
            self.connection.disable_monitor()
        except Exception as e:
            logger.warning('ZMQOutput.disconnect exception - error while disabling monitor: {}'.format(e))
        # close zmq socket
        self.connection.close()
        self.connected = False

    def __str__(self):
        return "zmq {}".format(self._out_endpoint)

    def __repr__(self):
        self._num_subscribers_lock.acquire()
        num_sub = self._num_subscribers
        self._num_subscribers_lock.release()
        return '<ZMQOutput: {} {}>'.format(self._out_endpoint, num_sub)

    def send(self, frame):
        """
        Send the frame to the output's connection
        """

        if frame.zmqinfo is None:
            # Reconstruct the ZMQ frame
            frame_header = "<HHIhh"

            datasize = len(frame.data)

            # ZMQ uses an integer: AACPLUS=1 MPEG_LAYER2=2
            encoder = 1 # This implies MPEG layer 2 EDI sources with ZMQ outputs won't work.
            version = 1

            header = struct.pack(frame_header, version, encoder, datasize, frame.audiolevel_left, frame.audiolevel_right)

            self.connection.send(header + frame.data, zmq.NOBLOCK)
        else:
            self.connection.send(frame.zmqinfo['rawframe'], zmq.NOBLOCK)

        # TODO handle exception due to noblock

class EDIOutput:
    STATE_DISCONNECTED = "disconnected"
    STATE_CONNECTING = "connecting"
    STATE_CONNECTED = "connected"

    """
    Output TCP client for EDI. Handles auto-reconnection
    """
    def __init__(self, output, version):
        self.protocol = "edi"
        self._version = version
        self.output = output
        self._host = output['host']
        self._port = output['port']
        self._state = EDIOutput.STATE_DISCONNECTED

        self._encoder = EDIFrameEncoder()

        self._sock = socket.socket()
        self._sock.setblocking(False)

        self._queue = bytearray()

        self._connect()

    def __str__(self):
        return "edi {}:{}".format(self._host, self._port)

    def _connect(self):
        # The only way to know if a socket is connected is to see if communication
        # succeeds
        self._set_state(EDIOutput.STATE_CONNECTING)

        self._sock.close()
        self._sock = socket.socket()
        self._sock.setblocking(False)

        try:
            self._sock.connect((self._host, self._port))
        except BlockingIOError:
            pass

    def _set_state(self, state):
        if self._state != state:
            logging.info("EDI output {}:{} state change: {} -> {}".format(self._host, self._port, self._state, state))
        self._state = state

    def is_connected(self):
        return self._state == EDIOutput.STATE_CONNECTED

    def stop(self):
        self._sock.close()
        self._queue = bytearray()
        self._set_state(EDIOutput.STATE_DISCONNECTED)

    def send(self, frame):
        if self._state == EDIOutput.STATE_DISCONNECTED:
            self._connect()

        # accumulate the data into our queue, since send() might not transmit all we ask it to
        if frame.ediinfo is not None:
            for rawframe in frame.ediinfo['rawframes']:
                self._queue.extend(rawframe)
        else:
            # From one frame (120ms) we build 5 AF (5x 24ms) packets
            if len(frame.data) % 5 != 0:
                raise RuntimeError("Cannot split frame data in 5: {}".format(len(frame.data)))

            chunk_len = int(len(frame.data) / 5)
            for ix in range(0, len(frame.data), chunk_len):
                chunk = frame.data[ix:ix+chunk_len]

                audiolevels = (frame.audiolevel_left, frame.audiolevel_right)
                version = "odroute {}".format(self._version)

                af_packet = self._encoder.encode_edi_frame(chunk, audiolevels, version)
                self._queue.extend(af_packet)

        if self._state == EDIOutput.STATE_CONNECTING or self._state == EDIOutput.STATE_CONNECTED:
            try:
                sent_bytes = self._sock.send(self._queue)
                self._queue = self._queue[sent_bytes:]
                self._set_state(EDIOutput.STATE_CONNECTED)

            except BlockingIOError:
                pass
            except BrokenPipeError:
                self._connect()
            except ConnectionResetError:
                self._connect()
            except ConnectionRefusedError:
                self._connect()
            except Exception as e:
                logging.error("Unknown exception in EDI send: {}".format(e))



