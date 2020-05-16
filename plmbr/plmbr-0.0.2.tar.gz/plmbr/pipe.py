""" Essential building blocks for a plmbr. """
from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Generic, TypeVar, List, Union, Sequence
from itertools import tee, chain

I = TypeVar('I')
O = TypeVar('O')
T = TypeVar('T')


def _split(items: Iterator[I], pipes: 'List[Pipe[I, O]]') -> Iterator[O]:
    return chain.from_iterable(
        pipe.pipe(items)
        for items, pipe
        in zip(tee(items, len(pipes)), pipes)
    )


class _Tap(Generic[I]):
    def __init__(self, items: Iterator[I]):
        self.items = items

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.items)

    def __sub__(self, pipe: 'Pipe[I, O]') -> '_Tap[O]':
        return _Tap(pipe(self))

    def __add__(self, pipes: 'List[Pipe[I, O]]') -> '_Tap[O]':
        return _Tap(_split(self, pipes))

    def __gt__(self, pipe: 'Pipe[I, O]'):
        pipe.flush(self)


class Pipe(ABC, Generic[I, O]):
    """ 
    A base class for all pipes.
    """
    @abstractmethod
    def pipe(self, items: Iterator[I]) -> Iterator[O]: ...

    def flush(self, items: Iterator[I]):
        for i in self(items):
            ...

    def __call__(self, items: Iterator[I]) -> Iterator[O]:
        return self.pipe(items)

    def __rsub__(self, items: Union[Sequence[I], Iterable[I]]) -> '_Tap[O]':
        return _Tap(self((i for i in items)))

    def __sub__(self, pipe: 'Pipe[O, T]') -> 'Pipe[I, T]':
        return _PipePipe(self, pipe)

    def __add__(self, pipes: 'List[Pipe[O, T]]') -> 'Pipe[I, T]':
        return _PipePipes(self, pipes)


class _PipePipe(Pipe[I, T]):
    def __init__(self, p: Pipe[I, O], q: Pipe[O, T]):
        self.p = p
        self.q = q

    def pipe(self, items: Iterator[I]) -> Iterator[T]:
        return self.q(self.p(items))


class _PipePipes(Pipe[I, T]):
    def __init__(self, p: Pipe[I, O], ps: List[Pipe[O, T]]):
        self.p = p
        self.ps = ps

    def pipe(self, items: Iterator[I]) -> Iterator[T]:
        return _split(self.p(items), self.ps)
