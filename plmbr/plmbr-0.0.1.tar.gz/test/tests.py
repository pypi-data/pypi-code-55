from plmbr.pipe import Pipe, I
from typing import Any, Iterator
import os
from pathlib import Path
from itertools import zip_longest


def path(file):
    return str(
        Path(os.path.dirname(os.path.abspath(__file__))) / file
    )


def check(exp, msg=''):
    assert exp, msg


class validate(Pipe[I, I]):
    def __init__(self, validator: Iterator):
        self.validator = validator

    def pipe(self, items: Iterator[I]) -> Iterator[I]:
        for item, valid in zip_longest(items, self.validator):
            valid(item)
            yield item
