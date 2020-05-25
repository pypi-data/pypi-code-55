import zmq

from keios_zmq.log_provider import LogProvider
from keios_zmq.dispatcher import Dispatcher
from keios_zmq.zmq_server import ZMQServer


class KeiosZMQ(ZMQServer):
    """
    Blocking KeiosZMQ server
    """
    log = LogProvider.get_logger("blocking-keios-zmq-server")

    def __init__(self, port: int,
                 message_handler: Dispatcher):
        self._port = port
        self._zmq_context = zmq.Context()
        self._socket = self._zmq_context.socket(zmq.ROUTER)
        self._socket.bind("tcp://*:{}".format(port))
        self._socket.setsockopt(zmq.LINGER, 1)
        self._message_handler = message_handler
        self.stopped = False

    def internal_handler(self):
        while not self.stopped:
            try:
                identity, messages = self.destruct(self._socket.recv_multipart())
                self.log.debug("Msg received - identity: {}, data: {}".format(identity, messages))
                self._socket.send_multipart(self.construct(identity, self._message_handler.execute(messages)))
            except zmq.error.ContextTerminated as e:
                pass  # this error is expected from .close()

    def start_server(self):
        self.log.info(f"Blocking-zmq-server started on port: {self._port}")
        self.internal_handler()

    def close(self):
        self.stopped = True
        self._socket.close()
        self._zmq_context.term()
