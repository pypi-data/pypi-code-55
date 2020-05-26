import datetime
import logging
import random

from abc import ABC, abstractmethod

from lemmings.utils.parsing import duration


class RPS(ABC):
    def __init__(self, max_duration=None):
        self.duration = duration(max_duration)

    def update_duration(self, new_duration):
        self.duration = duration(new_duration)

    def check_duration(self, offset):
        return self.duration and duration(offset) > self.duration

    @abstractmethod
    def sleep_time(self, offset):
        pass

    def __str__(self):
        if self.duration:
            return f" in duration {self.duration}"
        return ""


class NoLimits(RPS):

    def sleep_time(self, offset):
        if self.check_duration(offset):
            return None
        return datetime.timedelta(0)

    def __str__(self):
        return f"Rate[no limits{super().__str__()}]"

class Constant(RPS):
    def __init__(self, rps, max_duration=None):
        super().__init__(max_duration)
        self.rps = rps

    def sleep_time(self, offset):
        if self.check_duration(offset):
            return None
        return datetime.timedelta(seconds=1 / self.rps)

    def __str__(self):
        return f"Rate[const {self.rps} r/s{super().__str__()}]"

class InRange(RPS):
    def __init__(self, min_wait, max_wait=None, max_duration=None):
        super().__init__(max_duration)
        self.min_wait = min_wait
        self.max_wait = max_wait if max_wait else min_wait

    def sleep_time(self, offset):
        if self.check_duration(offset):
            return None
        return self.min_wait + random.random() * (self.max_wait - self.min_wait)

    def __str__(self):
        return f"Rate[in range [{self.min_wait},{self.min_wait}] r/s{super().__str__()}]"

class Linear(RPS):
    def __init__(self, min_rps, max_rps, max_duration):
        super().__init__(max_duration)
        self.min_rps = min_rps
        self.max_rps = max_rps if max_rps else min_rps

    def calc_time(self, offset):
        perc = duration(offset).total_seconds() / self.duration.total_seconds()
        r = self.min_rps + perc*(self.max_rps-self.min_rps)
        w = 1/r if r > 0 else 0
        logging.debug(f"offset: {offset} [{perc*100:.2f}%], rps for [{self.min_rps}, {self.max_rps}] = {r}, wait {w:.3f}")
        return w

    def sleep_time(self, offset):
        if self.check_duration(offset):
            return None
        return datetime.timedelta(seconds=self.calc_time(offset))

    def __str__(self):
        return f"Rate[linear [{self.min_rps},{self.max_rps}] r/s{super().__str__()}]"

class Complex(RPS):
    def __init__(self, *rps):
        sum = duration(0)
        for r in rps:
            if not r.duration:
                raise Exception()
            sum += r.duration
        super().__init__(sum)
        self.list = rps

    def sleep_time(self, offset):
        for r in self.list:
            x = r.sleep_time(offset)
            if x:
                return x
            offset -= r.duration
        return None

    def __str__(self):
        return f"Rate[{', '.join(map(str, self.list))}]"
