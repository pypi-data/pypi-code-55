from datetime import datetime, timedelta

from decopatch import F_ARGS, F_KWARGS, WRAPPED, function_decorator


GLOBAL_CACHE = {}


class ExpiredData(Exception):
    pass


@function_decorator
def cache(
    expire_secs=None,
    func=WRAPPED,
    func_args=F_ARGS,
    func_kwargs=F_KWARGS,
    _cache=GLOBAL_CACHE,
):
    """
    Cache decorator.

    Usage:
        - @cache
        - @cache()
        - @cache(expire_secs=300)

    Note: this is implemented with decopatch.function_decorator which allows writing
    the replacement function in one single pass.
    """
    key = f'{func.__name__}:{func_args!r}:{func_kwargs!r}'

    now = datetime.now()
    expire_time = None
    if expire_secs:
        expire_time = now + timedelta(seconds=expire_secs)

    try:
        data = _cache[key]

        if data['expire'] is not None and data['expire'] < now:
            _cache.pop(key, None)
            raise ExpiredData

        value = data['value']

    except (KeyError, ExpiredData):
        value = func(*func_args, **func_kwargs)
        _cache[key] = {'value': value, 'expire': expire_time}

    return value


def clear_cache(_cache=GLOBAL_CACHE):
    _cache.clear()
