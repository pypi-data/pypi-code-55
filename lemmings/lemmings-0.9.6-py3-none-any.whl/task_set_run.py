import asyncio
import collections
import random
import time
from datetime import timedelta

from lemmings.task import Task
from lemmings.utils import duration
from lemmings.utils.coroutine import duration2sec


class TaskSetRun:
    def __init__(self, worker, task_set):
        self.worker = worker
        self.task_set = task_set
        self.total = len(self.task_set.tasks)

        self.current = -1  # idx in task_set of current task (for generator)
        self.generated = 0  # current count of generated tasks
        for item in self.task_set.tasks:
            item.set_test_plan(task_set)
        # self.start_time = time.time()

    @property
    def shared(self):
        return self.worker.shared_state

    def log(self, msg, comment=""):
        self.worker.log(msg, comment)

    async def sleep(self, _duration=None, comment=""):
        if not _duration:
            _duration= timedelta(seconds=random.random())
        _duration = duration(_duration) # autoconvert
        if _duration.total_seconds() > 3:
            self.log(f"SLEEP FOR {_duration}", comment)
        await asyncio.sleep(duration2sec(_duration))

    async def in_duration(self, _duration, times) -> collections.AsyncIterable:
        times = int(times)
        _duration = duration(_duration) # auto convert from int, str
        start_time = time.time()
        for step in range(times):
            yield step
            elapsed = timedelta(seconds=time.time() - start_time)
            if times - step > 1:
                sleep_time = (_duration - elapsed) / (times - step - 1)
                await self.sleep(sleep_time, f"after #{step + 1} step of {times} total in duration {_duration}")

    # def rps_in_duration(self, _duration, rps) -> collections.AsyncIterable:
    #     _duration = duration(_duration) # auto convert from int, str
    #     return self.in_duration(_duration, _duration.total_seconds() * rps)

    def with_rps(self, rps):
        class RPS:
            def __init__(self, rps, runner):
                self.rps = rps
                self.runner = runner

            def in_duration(self, _duration) -> collections.AsyncIterable:
                _duration = duration(_duration) # auto convert from int, str
                return self.runner.in_duration(_duration, _duration.total_seconds() * self.rps)

        return RPS(rps, self)

    def with_rpm(self, rpm):
        return self.with_rps(rpm / 60)

    @property
    def is_ordered(self):
        return self.task_set.is_sequence

    @property
    def tasks(self):
        return self.task_set.tasks

    @property
    def sorted_tasks(self):
        return sorted(self.tasks, key=lambda t: t.order)

    def setup_task(self):
        return Task(self.task_set.setup, system=True, comment="Setup * ")

    def teardown_task(self):
        return Task(self.task_set.teardown, system=True, comment="Teardown * ")

    def schedule(self, with_tear_down=False):
        offset = duration(0)
        res = [(offset, self.setup_task())]
        while True:
            sleep_time = self.task_set.rps.sleep_time(offset)
            if sleep_time is None: # finish
                # self.log(f"FINISH! {sleep_time} @ {offset}: {self.task_set.rps}")
                break
            offset += sleep_time

            # stop by TaskSet's 'max_run' parameter
            if 0 < self.task_set.runs < self.generated:
                break
            if not self.is_ordered:
                s = self.weighted_random()
                res.append((offset, s))
                continue
            s = self.ordered()
            if s:
                res.append((offset, s))
            else:
                break
        if with_tear_down:
            res.append((offset, self.teardown_task()))

        # def f(s):
        #     off, task = s
        #     return f"({off}: {task})"
        # self.log(f"scheduled: {', '.join(map(f, res))}")
        return res

    def _schedule_teardown(self):
        self.in_processing = False
        return Task(self.task_set.teardown, system=True, comment="Teardown * ")

    def weighted_random(self):
        n = random.uniform(0, self.task_set.weight_total)
        for idx, item in enumerate(self.tasks):
            if n < item.weight:
                self.current = idx
                self.generated += 1
                return item
            n = n - item.weight
        return None

    def ordered(self):
        self.current += 1
        if self.current >= self.total:
            return None
        self.generated += 1
        return self.sorted_tasks[self.current]
