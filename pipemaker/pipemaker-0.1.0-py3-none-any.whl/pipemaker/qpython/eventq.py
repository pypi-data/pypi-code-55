from ..utils.share import create_client, create_server
import pipemaker.master as m
from queue import Queue
import logging

log = logging.getLogger(__name__)


class Dictq:
    """ dict of queues. use queue blocking to wait for a key """

    def __init__(self):
        self.d = dict()

    def get(self, key):
        """ wait for key """
        self.d[key] = Queue()
        return self.d[key].get()

    def put(self, key, value):
        """ trigger key """
        self.d.setdefault(key, Queue())
        self.d[key].put(value)


class Eventq:
    """ wait for response. may include data.

    Usage:
        wait for an event to happen
        send request to a queue. wait for data to be returned.
    """

    @classmethod
    def start_server(self):
        self.dq = Dictq()
        create_server(self.dq, port=m.CONFIG.eventq_port)

    def __init__(self, key):
        """
        :param key: item to wait for e.g name of file OR random string
        """
        self.key = key

    def start(self, **kwargs):
        dq = create_client(port=m.CONFIG.eventq_port)
        return dq.get(self.key)


class EventqP:
    """ Trigger event. may also include data.
    """

    def __init__(self, key, body="", **kwargs):
        """
        :param key: unique routing key e.g name of file OR random string
        :param body: data to be returned to consumer. None if just notifying event happened.
        """
        dq = create_client(port=m.CONFIG.eventq_port)
        dq.put(key, body)
