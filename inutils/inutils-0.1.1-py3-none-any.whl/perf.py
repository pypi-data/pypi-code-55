from functools import partial
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


if __name__ == '__main__':
    tries = 1_000
    timer = partial(
        timeit,
        setup='from inutils import chunkify; iterable = [1] * 1_000_000',
        number=tries,
        globals=globals(),
    )
    s = '{}\tavg {:.2f}µs\t({} tries)'
    res = timer(stmt='list(grouper(iterable, 10_000))')
    print(s.format('grouper\t', (res / tries) * 1e6, tries))

    res = timer(stmt='list(chunkify(iterable, 10_000))')
    print(s.format('chunkify', (res / tries) * 1e6, tries))
