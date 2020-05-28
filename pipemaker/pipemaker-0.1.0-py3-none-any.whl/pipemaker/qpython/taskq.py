from ..utils.share import create_client, create_server
import pipemaker.master as m
from threading import Thread
from queue import Queue
import logging

log = logging.getLogger(__name__)


class Taskq:
    """ Consumer for python event queue """

    @classmethod
    def start_server(self):
        self.q = Queue()
        create_server(self.q, port=m.CONFIG.taskq_port)

    def __init__(self, taskdb):
        self.taskdb = taskdb
        self.finished = False
        self.start()

    def start(self):
        """ background thread to consume messages """

        def target():
            try:
                while True:
                    body = self.q.get()
                    if self.finished:
                        break
                    getattr(self.taskdb, body["event"])(body)
            except:
                log.exception(f"Error processing event {body}")

        t = Thread(target=target, daemon=True, name=__name__)
        t.start()

    def stop(self):
        self.taskdb.clear()
        self.finished = True
        # unblock empty queue
        self.q.put("")


class TaskqP:
    """ Producer for python event queue """

    def __init__(self, **kwargs):
        self.q = create_client(port=m.CONFIG.taskq_port)

    def put(self, body):
        self.q.put(body)
