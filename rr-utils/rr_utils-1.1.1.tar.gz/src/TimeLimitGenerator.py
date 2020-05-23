import time


class TimeLimitGenerator:
    def __init__(self, time_limit_seconds, func):
        self._time_limit = time_limit_seconds
        self._func = func

    def get_counter(self):
        return self._counter

    def __iter__(self):
        self._counter = 0
        self._start_time = time.time()
        self._prev_time = self._start_time
        return self

    def __next__(self):
        current_time = time.time()
        delta_time_sec = current_time - self._start_time
        if delta_time_sec > self._time_limit:
            raise StopIteration

        since_prev_time = current_time - self._prev_time
        self._prev_time = current_time
        result = self._func(self._counter, delta_time_sec, since_prev_time)

        self._counter += 1
        return result
