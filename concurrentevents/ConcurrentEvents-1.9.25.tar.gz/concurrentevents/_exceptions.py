class EventError(Exception):
    """Standard Event Exception"""


class Cancel(EventError):
    """Raised when an event is canceled"""
