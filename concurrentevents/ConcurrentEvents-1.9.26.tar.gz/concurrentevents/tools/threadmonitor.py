from functools import wraps

_monitoring = {}


def thread_monitor(f):
    """
    A decorator to bse used in monitoring functions that have any possibility of causing a deadlock

    Default implementation is under ConcurrentWorkLimiter and ResourceManager as both have
    functionality where threads can interact indirectly

    Debug can be used through this by simply printing the dictionary and it will display how many of each
    monitored function is running at any point in time

    Args:
        :param f: a function which will be added to the monitoring dict
        :type f: class:`function`
    """

    _name = f"{f.__module__.split('.')[-1]}.{f.__name__}()"
    _monitoring.update({_name: 0})

    @wraps(f)
    def wrapper(*args, **kwargs):
        error = None

        _monitoring[_name] += 1

        try:
            result = f(*args, **kwargs)
        except Exception as e:
            error = e
            result = None

        _monitoring[_name] -= 1

        if error:
            raise error

        return result
    return wrapper
