from typing import Callable, Optional
from types import FrameType
import signal
from contextlib import contextmanager

def __default_timeout_handler(signal_number: int, frame: Optional[FrameType]):
    raise Exception("Operation has timed out")

# If you decide to use a custom handler, keep in mind, that the handler will be called with 2 arguments:
#   - int:                  the signal number
#   - Optional[FrameType]:  the current stack frame (None or a frame object)
@contextmanager
def timeout(_timeout: int, timeout_handler: Callable = __default_timeout_handler):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(_timeout)

    try:
        yield
    except:
        raise
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        signal.alarm(0)

# If you decide to use a custom handler, keep in mind, that the handler will be called with 2 arguments:
#   - int:                  the signal number
#   - Optional[FrameType]:  the current stack frame (None or a frame object)
def run(func: Callable, _timeout: int, timeout_handler: Callable = __default_timeout_handler):
    with timeout(_timeout, timeout_handler=timeout_handler):
        return func()

def partial(func: Callable, *args, **kwargs):
    from functools import partial as _partial

    return _partial(func, *args, **kwargs)