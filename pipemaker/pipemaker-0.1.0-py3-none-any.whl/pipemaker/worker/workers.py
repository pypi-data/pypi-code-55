import os
from time import sleep
from ..utils import get_name
import pipemaker.master as m
import logging

log = logging.getLogger(__name__)


class Workers:
    def __init__(self, n, ch):
        self.workers = []
        self.n_workers = n
        self.ch = ch

    def start(self):
        """ starts required number of workers to get n_workers"""
        try:
            n = self.n_workers
            os.environ["NUMEXPR_NUM_THREADS"] = str(n)
            name = get_name()
            for i in range(n):
                if i == 0:
                    log.info(f"starting workers {name} n={n}")
                w = m.Workerq()
                w.start(f"{name}_{i}")
                self.workers.append(w)
            # wait for workers to start. tasks launched on rabbitmq before consumers ready will be ignored.
            # python queue does not reveal consumers
            if hasattr(m.Workerq, "consumers"):
                while m.Workerq.consumers(self.ch) < n:
                    sleep(1)
        except:
            log.exception("Error starting workers")

    def stop(self):
        """ terminate workerq and worker processes (which would continue independently of the queue) """
        if self.ch:
            self.ch.queue_delete("Workerq")
        for w in self.workers:
            w.stop()
