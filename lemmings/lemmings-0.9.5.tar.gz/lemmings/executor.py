import logging
import os
from multiprocessing import Process, Pool

from prometheus_client import multiprocess

from lemmings.worker import Worker
from lemmings.statistics import  Statistics
from lemmings.utils import _num, ProcessStat
from lemmings.utils.const import DONE, FAIL

class TestExecutor:
    def __init__(self, ansi_colors=False, debug=False):
        self.workers = []
        self.ansi_colors = ansi_colors
        self.debug = debug
        self.test_plans = 0
        self.available_plans = {}

    def add_test_plan(self, task_set, workers=1):
        logging.info(f"schedule {workers} worker(s) for test plan: {task_set}")
        for a in range(workers):
            self.workers.append(Worker(f"thread{a}", task_set, ansi_colors=self.ansi_colors, debug=self.debug))
        self.test_plans += 1
        return self

    def start_all(self, shared_state):
        """
        :param args: list of shared variables between workers[processes]
        """
        stat = Statistics()
        with Pool(len(self.workers)) as p:
            procs = [Process(name=f"Worker{w.id}", target=self.start_process, args=[w, stat, shared_state]) for w in self.workers]
            for p in procs: p.start()
            for p in procs: p.join()
            pids = [x.pid for x in procs]
            for pid in pids:
                multiprocess.mark_process_dead(pid)
            self.done(stat)
        logging.info(f"Executor workers in child processed were finished")

    def start_process(self, worker, stat, shared_state):
        shared_state.init_multiprocess()
        worker.set_statistics(stat)
        worker.set_shared(shared_state)
        id, name = worker.id, worker.name
        task_set = worker.task_set.__class__.__name__
        worker.set_title(f"{task_set} [pid {os.getpid():6d}<:{os.getppid()}]")
        worker.set_process_name(f"{task_set}_{id}")
        worker.log("start process")
        worker.gc = ProcessStat()
        worker.execute()

    def done(self, stat):
        logging.info(f"merged results: {_num(stat.shared_executed)} {DONE},"
              f" {_num(stat.shared_failed)} {FAIL} "
              f"[{_num(stat.shared_total)} total]")
