from typing import Optional

__all__ = ['BaseXToolsException', 'NotFound', 'TooManyEdits']


class BaseXToolsException(Exception):
    def __init__(self, message, code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.code = code

    def __eq__(self, other):
        return isinstance(other, BaseXToolsException) \
            and str(self) == str(other) \
            and self.code == other.code


class NotFound(BaseXToolsException):
    pass


class TooManyEdits(BaseXToolsException):
    pass