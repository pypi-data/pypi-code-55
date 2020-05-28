""" simple example """

from time import sleep

try:
    __IPYTHON__
    from tqdm.notebook import tqdm
except:
    from tqdm import tqdm
from pipemaker.worker.task import progress

import logging

log = logging.getLogger(__name__)


def _delay(delay=60):
    """ add a delay to simulate long running task """
    delay = list(range(delay))
    for i in tqdm(delay):
        sleep(1)
        progress(i, len(delay))


def make_odd(low, delay=60):
    """ return list of 3 odd numbers """
    if low % 2 == 0:
        low = low + 1
    r = range(low, low + 6, 2)
    _delay(delay)
    return list(r)


def make_even(low, delay=60):
    """ return list of 3 even numbers """
    if low % 2 != 0:
        low = low + 1
    r = range(low, low + 6, 2)
    _delay(delay)
    return list(r)


def make_oddeven(odd, even, delay=60):
    """ concatenate odd and even """
    r = odd + even
    _delay(delay)
    return sorted(r)
