import sys


def get_argv(idx, default):
    try:
        return sys.argv[idx]
    except IndexError:
        return default
