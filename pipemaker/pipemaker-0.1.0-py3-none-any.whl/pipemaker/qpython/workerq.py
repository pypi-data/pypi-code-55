#!/usr/bin/env python
import multiprocessing as mp
from ..utils.share import create_client, create_server
import pipemaker.master as m
from queue import Queue
import logging

log = logging.getLogger(__name__)


class Workerq:
    """ a task queue that executes one task at a time """

    @classmethod
    def start_server(self):
        """ outside process as needed before taskq started
         """
        self.q = Queue()
        create_server(self.q, port=m.CONFIG.workerq_port)

    def start_process(self):
        # default logging plus queue
        from ..utils.defaultlog import log
        from ..master import loghandler

        rootlog = logging.getLogger()
        rootlog.addHandler(loghandler.SharedQueueHandler())

        q = create_client(port=m.CONFIG.workerq_port)
        while True:
            body = q.get()
            if body == "_sentinel":
                break
            try:
                body.taskqP = m.TaskqP()
                body.run()
            except:
                log.exception(f"Unable to handle message={body}")

    def start(self, name=""):
        """ create background process as workers need to utlise cpus
        """
        # consume process
        self.p = mp.Process(target=self.start_process, daemon=True, name=name)
        self.p.start()

    def stop(self):
        # if idle then stop cleanly e.g. to allow pytest coverage to work.
        self.q.put("_sentinel")

        # otherwise terminate anyway
        self.p.terminate()
        self.p.join()


class WorkerqP:
    def __init__(self, **kwargs):
        self.q = create_client(port=m.CONFIG.workerq_port)

    def put(self, body=""):
        self.q.put(body)
