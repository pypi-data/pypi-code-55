import asyncio
import functools
import math
import time

from prometheus_client import values
from prometheus_client.metrics import MetricWrapperBase

_BUFFER_SIZE = 512

default_timer = time.perf_counter

class QTimer(object):
    def __init__(self, callback):
        self._callback = callback

    def _new_timer(self):
        return self.__class__(self._callback)

    def __enter__(self):
        self._start = default_timer()

    def __exit__(self, typ, value, traceback):
        duration = max(default_timer() - self._start, 0)
        self._callback(duration)

    def __call__(self, f):
        if asyncio.iscoroutinefunction(f):
            @functools.wraps(f)
            async def wrapper_timer(*args, **kwargs):
                with self._new_timer():
                    return await f(*args, **kwargs)
            return wrapper_timer
        else:
            @functools.wraps(f)
            def wrapper_timer(*args, **kwargs):
                with self._new_timer():
                    return f(*args, **kwargs)
            return wrapper_timer

class QuantileSummary(MetricWrapperBase):
    _type = 'summary'
    _reserved_labelnames = ['quantile']

    def _metric_init(self):
        self._count = values.ValueClass(self._type, self._name, self._name + '_count', self._labelnames, self._labelvalues)
        self._sum = values.ValueClass(self._type, self._name, self._name + '_sum', self._labelnames, self._labelvalues)
        self._created = time.time()

    def observe(self, amount):
        self._count.inc(1)
        self._sum.inc(amount)

    def time(self):
        return QTimer(self.observe)

    def route_time(self):
        return QTimer(self.observe)

    def _child_samples(self):
        return (
            ('_count', {}, self._count.get()),
            ('_sum', {}, self._sum.get()),
            ('_created', {}, self._created))


class Estimator(object):
    """Estimator is not concurrency safe."""

    def __init__(self, *invariants):
        """ Attributes:
            invariants: A list of floating point doubles containing the target
                quantile value and allowed error.   [(0.5, 0.01), (0.99, 0.001)]
                are the default if none are provided, signifying that the median
                will be provided at a one percent error limit and the 99th
                percentile at the a 0.1 percent error limit.
        """
        if not invariants:
            self._invariants = _DEFAULT_INVARIANTS
        else:
            self._invariants = [_Quantile(q, e) for (q, e) in invariants]
        self._buffer = []
        self._head = None
        self._observations = 0
        self._sum = 0

    def observe(self, value):
        """Samples an observation's value.
        Args:
            value: A numeric value signifying the value to be sampled.
        """
        self._buffer.append(value)
        if len(self._buffer) == _BUFFER_SIZE:
            self._flush()

        self._observations += 1
        self._sum += value

    def query(self, rank):
        self._flush()

        current = self._head
        if not current:
            return 0

        mid_rank = math.floor(rank * self._observations)
        max_rank = mid_rank + math.floor(self._invariant(mid_rank, self._observations) / 2)

        rank = 0.0
        while current._successor:
            rank += current._rank
            if rank + current._successor._rank + current._successor._delta > max_rank:
                return current._value

            current = current._successor

        return current._value

    def _flush(self):
        """Purges the buffer and commits all pending values into the estimator."""
        self._buffer.sort()
        self._replace_batch()
        self._buffer = []
        self._compress()

    def _replace_batch(self):
        """Incorporates all pending values into the estimator."""
        if not self._head:
            self._head, self._buffer = self._record(self._buffer[0], 1, 0, None), self._buffer[1:]

        rank = 0.0
        current = self._head

        for b in self._buffer:
            if b < self._head._value:
                self._head = self._record(b, 1, 0, self._head)

            while current._successor and current._value < b:
                rank += current._rank
                current = current._successor

            if not current._successor:
                current._successor = self._record(b, 1, 0, None)

            current._successor = self._record(b, 1, self._invariant(rank, self._observations)-1, current._successor)

    def _record(self, value, rank, delta, successor):
        """Catalogs a sample."""
        return _Sample(value, rank, delta, successor)

    def _invariant(self, rank, n):
        """Computes the delta value for the sample."""
        minimum = n + 1

        for i in self._invariants:
            delta = i._delta(rank, n)
            if delta < minimum:
                minimum = delta

        return math.floor(minimum)

    def _compress(self):
        """Prunes the cataloged observations."""
        rank = 0.0
        current = self._head

        while current and current._successor:
            if current._rank + current._successor._rank + current._successor._delta <= self._invariant(rank, self._observations):
                removed = current._successor

                current._value = removed._value
                current._rank += removed._rank
                current._delta = removed._delta
                current._successor = removed._successor

            rank += current._rank
            current = current._successor


class _Quantile(object):
    """_Quantile is an internal representation of an estimation target invariant.
    Attributes:
        quantile: A floating point value for the requested quantile along the [0, 1] interval.
        inaccuracy: A floating point value for the allowed error for the estimate along the [0, 1] interval.
    """
    def __init__(self, quantile, inaccuracy):
        self._quantile = quantile
        self._inaccuracy = inaccuracy
        self._coefficient_i = (2.0 * inaccuracy) / (1.0 - quantile)
        self._coefficient_ii = 2.0 * inaccuracy / quantile

    """Computes the delta for the observation."""
    def _delta(self, rank, n):
        if rank <= math.floor((self._quantile * n)):
            return self._coefficient_i * (n - rank)

        return self._coefficient_ii * rank



class _Sample(object):
    def __init__(self, value, rank, delta, successor):
        self._value = value
        self._rank = rank
        self._delta = delta
        self._successor = successor

_DEFAULT_INVARIANTS = [_Quantile(0.50, 0.01), _Quantile(0.99, 0.001)]
