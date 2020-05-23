import time


class StopWatch:
    def __init__(self, auto_start=True):
        self._start_time = None
        self._saved_time = None
        if auto_start:
            self.reset()

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return self

    def stop(self):
        self._saved_time = time.time() - self._start_time

    def reset(self):
        self._saved_time = None
        self._start_time = time.time()

    def get_start_time(self):
        return self._start_time

    def get_elapsed_time(self):
        if self._start_time is None:
            return None

        if self._saved_time is not None:
            return self._saved_time

        delta = time.time() - self._start_time
        return delta


