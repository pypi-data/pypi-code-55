import asyncio
import time

_DEFAULT_BASE_SLEEP = 2.0
_DEFAULT_MAX_SLEEP = 128.0
_DEFAULT_SLEEP_GROWTH = 2.0
_DEFAULT_TIMEOUT = None


class QcticResultTimeoutError(Exception):
    pass


def _raise_if_timeout(start, timeout):
    if timeout is None:
        return

    diff = time.time() - start

    if diff >= timeout:
        raise QcticResultTimeoutError(
            "Timeout exceeded ({} secs)".format(timeout))


def wait_result(job, **kwargs):
    sleep = kwargs.get("base_sleep", _DEFAULT_BASE_SLEEP)
    max_sleep = kwargs.get("max_sleep", _DEFAULT_MAX_SLEEP)
    sleep_growth = kwargs.get("sleep_growth", _DEFAULT_SLEEP_GROWTH)
    timeout = kwargs.get("timeout", _DEFAULT_TIMEOUT)
    start = time.time()

    while True:
        res = job.result(fetch=True)

        if res:
            return res

        _raise_if_timeout(start, timeout)
        time.sleep(sleep)
        sleep = min(sleep * sleep_growth, max_sleep)


async def wait_result_async(job, **kwargs):
    sleep = kwargs.get("base_sleep", _DEFAULT_BASE_SLEEP)
    max_sleep = kwargs.get("max_sleep", _DEFAULT_MAX_SLEEP)
    sleep_growth = kwargs.get("sleep_growth", _DEFAULT_SLEEP_GROWTH)
    timeout = kwargs.get("timeout", _DEFAULT_TIMEOUT)
    start = time.time()

    while True:
        res = await job.result_async(fetch=True)

        if res:
            return res

        _raise_if_timeout(start, timeout)
        await asyncio.sleep(sleep)
        sleep = min(sleep * sleep_growth, max_sleep)
