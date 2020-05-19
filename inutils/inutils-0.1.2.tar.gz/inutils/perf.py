from itertools import zip_longest
from timeit import timeit


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    Obtained at https://docs.python.org/dev/library/itertools.html#itertools-recipes
    """
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def timer(func, tries):
    res = timeit(
        stmt='foo({}(iterable, 10_000))'.format(func),
        setup="""
from inutils import chunkify
from more_itertools import chunked, ichunked
iterable = range(1_000_000)
def foo(iterable):
    for _ in iterable:
        pass
        """,
        number=tries,
        globals=globals(),
    )
    print('{:<10}avg {:.2f}µs'.format(func, (res / tries) * 1e6))


if __name__ == '__main__':
    tries = 10
    print('tries={}'.format(tries))
    timer('grouper', tries)
    timer('chunkify', tries)
    timer('chunked', tries)
    timer('ichunked', tries)
