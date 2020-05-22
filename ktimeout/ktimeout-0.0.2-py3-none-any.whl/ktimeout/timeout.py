from typing import Callable, Optional
from types import FrameType

def __default_timeout_handler(signal_number: int, frame: Optional[FrameType]):
    raise Exception("Operation has timed out")

# If you decide to use a custom handler, keep in mind, that the handler will be called with 2 arguments:
#   - int:                  the signal number
#   - Optional[FrameType]:  the current stack frame (None or a frame object)
def run(func: Callable, timeout: int, timeout_handler: Callable = __default_timeout_handler):
    import signal

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    func()