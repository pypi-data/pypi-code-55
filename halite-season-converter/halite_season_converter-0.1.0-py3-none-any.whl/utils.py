"""
Utilities for the package.
"""

from itertools import islice
from typing import Iterator, List, Any


def chunks(iterable: Iterator[Any], chunksize: int) -> Iterator[List[Any]]:
    """
    Breaks down an iterable into chunks.
    """
    iterable = iter(iterable)
    while True:
        chunk = tuple(islice(iterable, chunksize))
        if not chunk:
            return
        yield chunk
