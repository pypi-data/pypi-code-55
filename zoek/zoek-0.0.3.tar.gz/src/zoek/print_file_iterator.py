from typing import Iterator
from click import echo


def print_file_iterator(it: Iterator, showpath: bool) -> None:
    """Prints the elements of the provided iterator"""
    for file in it:
        # will f-stringing a condtional slow down execution at large numbers?
        echo(f'{file.path if showpath else file.name}')
