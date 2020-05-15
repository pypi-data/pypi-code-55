from kabooki.pipe import Pipe, I, O
from typing import Any, Callable, Dict, Iterator, List
import json
from itertools import islice
from tqdm import tqdm


class same(Pipe[I, I]):
    def pipe(self, it: Iterator[I]) -> Iterator[I]:
        return it


class json_loads(Pipe[str, Any]):
    def pipe(self, items: Iterator[str]) -> Iterator[Any]:
        return (json.loads(item) for item in items)


class json_dumps(Pipe[Any, str]):
    def pipe(self, items: Iterator[Any]) -> Iterator[str]:
        return (json.dumps(item) for item in items)


class batch(Pipe[I, List[I]]):
    def __init__(self, batch_size=64) -> None:
        self.batch_size = batch_size

    def pipe(self, it: Iterator[I]) -> Iterator[List[I]]:
        return iter(lambda: list(islice(it, self.batch_size)), [])


class unbatch(Pipe[List[I], I]):
    def pipe(self, lists: Iterator[List[I]]) -> Iterator[I]:
        return (item for l in lists for item in l)


class progress(Pipe[I, I]):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def pipe(self, it: Iterator[Any]) -> Iterator[Any]:
        return iter(tqdm(it, **self.kwargs))


class transform(Pipe[I, O]):
    def __init__(self, f: Callable[[I], O]):
        self.f = f

    def pipe(self, items: Iterator[I]) -> Iterator[O]:
        for item in items:
            yield self.f(item)


class keep(Pipe[I, I]):
    def __init__(self, filter):
        self.filter = filter

    def pipe(self, it: Iterator[I]) -> Iterator[I]:
        return filter(self.filter, it)


class drop_fields(Pipe[Dict[str, Any], Dict[str, Any]]):
    def __init__(self, *fields: str):
        self.fields = fields

    def pipe(self, items: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        for item in items:
            for field in self.fields:
                del item[field]

            yield item


class uniq(Pipe[Dict[str, Any], Dict[str, Any]]):
    def __init__(self, *fields: str):
        self.fields = fields
        self.set: set = set()

    def pipe(self, items: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        for item in items:
            i = frozenset({field: item[field] for field in self.fields}.items())
            if i in self.set:
                continue

            self.set.add(i)
            yield item


class log(Pipe[I, I]):
    def pipe(self, items: Iterator[I]) -> Iterator[I]:
        for item in items:
            print(item)
            yield item


class save(Pipe[I, I]):
    def __init__(self, file) -> None:
        self.file = file

    def pipe(self, items: Iterator[I]):
        with open(self.file, 'w') as f:
            for item in items:
                print(item, file=f)
                yield item
