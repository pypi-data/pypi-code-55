from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Generic, TypeVar, List, Union, Sequence
from itertools import tee, chain

I = TypeVar('I')
O = TypeVar('O')
T = TypeVar('T')


def split(items: Iterator[I], pipes: 'List[Pipe[I, O]]') -> Iterator[O]:
    return chain.from_iterable(
        pipe.pipe(items)
        for items, pipe
        in zip(tee(items, len(pipes)), pipes)
    )


class Tap(Generic[I]):
    def __init__(self, items: Iterator[I]):
        self.items = items

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.items)

    def __sub__(self, pipe: 'Pipe[I, O]') -> 'Tap[O]':
        return Tap(pipe(self))

    def __add__(self, pipes: 'List[Pipe[I, O]]') -> 'Tap[O]':
        return Tap(split(self, pipes))

    def __gt__(self, pipe: 'Pipe[I, O]'):
        pipe.flush(self)


class Pipe(ABC, Generic[I, O]):

    @abstractmethod
    def pipe(self, items: Iterator[I]) -> Iterator[O]: ...

    def flush(self, items: Iterator[I]):
        for i in self(items):
            ...

    def __call__(self, items: Iterator[I]) -> Iterator[O]:
        return self.pipe(items)

    def __rsub__(self, items: Union[Sequence[I], Iterable[I]]) -> 'Tap[O]':
        return Tap(self((i for i in items)))

    def __sub__(self, pipe: 'Pipe[O, T]') -> 'Pipe[I, T]':
        return PipePipe(self, pipe)

    def __add__(self, pipes: 'List[Pipe[O, T]]') -> 'Pipe[I, T]':
        return PipePipes(self, pipes)


class PipePipe(Pipe[I, T]):
    def __init__(self, p: Pipe[I, O], q: Pipe[O, T]):
        self.p = p
        self.q = q

    def pipe(self, items: Iterator[I]) -> Iterator[T]:
        return self.q(self.p(items))


class PipePipes(Pipe[I, T]):
    def __init__(self, p: Pipe[I, O], ps: List[Pipe[O, T]]):
        self.p = p
        self.ps = ps

    def pipe(self, items: Iterator[I]) -> Iterator[T]:
        return split(self.p(items), self.ps)
