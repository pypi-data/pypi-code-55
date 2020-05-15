from abc import ABC, abstractmethod
from typing import Iterator, Generic, TypeVar, List, Any
from itertools import tee

I = TypeVar('I')
O = TypeVar('O')
T = TypeVar('T')


class Tap(Generic[I]):
    def __init__(self, it: Iterator[I]):
        self.it = it

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.it)

    def __sub__(self, pipe: 'Pipe[I, O]') -> 'Tap[O]':
        return Tap(pipe(self))

    def __add__(self, sinks: 'List[Sink[I]]'):
        for it, sink in zip(tee(self, len(sinks)), sinks):
            sink.sink(it)

    def __gt__(self, sink: 'Sink[I]'):
        sink.sink(self)


class Pipe(ABC, Generic[I, O]):

    @abstractmethod
    def pipe(self, it: Iterator[I]) -> Iterator[O]: ...

    def __call__(self, it: Iterator[I]) -> Iterator[O]:
        return self.pipe(it)

    def __rsub__(self, it: Iterator[I]) -> 'Tap[O]':
        return Tap(self(it))

    def __sub__(self, pipe: 'Pipe[O, T]') -> 'Pipe[I, T]':
        return PipePipe(self, pipe)

    def __add__(self, sinks: 'List[Sink[O]]') -> 'Sink[I]':
        return PipeSinks(self, sinks)

    def __gt__(self, sink: 'Sink[O]') -> 'Sink[I]':
        return PipeSink(self, sink)


class PipePipe(Pipe[I, T]):
    def __init__(self, p: Pipe[I, O], q: Pipe[O, T]):
        self.p = p
        self.q = q

    def pipe(self, it: Iterator[I]) -> Iterator[T]:
        return self.q(self.p(it))


class Sink(Generic[I]):
    @abstractmethod
    def sink(self, it: Iterator[I]): ...


class PipeSink(Sink[I]):
    def __init__(self, pipe: Pipe[I, O], sink: Sink[O]):
        self.p = pipe
        self.s = sink

    def sink(self, it: Iterator[I]):
        self.s.sink(self.p(it))


class PipeSinks(Sink[I]):
    def __init__(self, pipe: Pipe[I, O], sinks: List[Sink[O]]):
        self.p = pipe
        self.sinks = sinks

    def sink(self, it: Iterator[I]):
        for o, sink in zip(tee(self.p(it), len(self.sinks)), self.sinks):
            sink.sink(o)
