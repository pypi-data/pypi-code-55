"""Exception types for PySpark-config errors."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import traceback

OK = 0
CANCELLED = 1
UNKNOWN = 2
INVALID_ARGUMENT = 3
DEADLINE_EXCEEDED = 4
NOT_FOUND = 5
ALREADY_EXISTS = 6
PERMISSION_DENIED = 7
UNAUTHENTICATED = 16
RESOURCE_EXHAUSTED = 8
FAILED_PRECONDITION = 9
ABORTED = 10
OUT_OF_RANGE = 11
UNIMPLEMENTED = 12
INTERNAL = 13
UNAVAILABLE = 14
DATA_LOSS = 15


class OpError(Exception):
    """
    A generic error that is raised when Pyspark_config execution fails.
    """

    def __init__(self, message, error_code, error=None):
        """Creates a new `OpError` indicating that a particular op failed.
        Args:
          op: The `ops.Operation` that failed, if known; otherwise None.
          message: The message string describing the failure.
          error_code: The error code describing the error.
        """
        super(OpError, self).__init__()
        self._message = message
        self._error_code = error_code
        self._error = error


    @property
    def message(self):
        """The error message that describes the error."""
        return self._message

    @property
    def error_code(self):
        """The integer error code that describes the error."""
        return self._error_code

    @property
    def error(self):
        """The external error which is reused, if available."""
        return self._error

    def __str__(self):
        if self.error:
            output=["%s\n\nOriginal stack trace:\n" % self.message]
            return "".join(output)
        else:
            return self.message


class UnknownError(OpError):
    """Unknown error.
    An example of where this error may be returned is if a Status value
    received from another address space belongs to an error-space that
    is not known to this address space. Also, errors raised by APIs that
    do not return enough error information may be converted to this
    error.
    """

    def __init__(self, op, message):
        """Creates an `UnknownError`."""
        super(UnknownError, self).__init__(message, error_code=UNKNOWN)


class InvalidArgumentError(OpError):
    """
    Raised when an operation receives an invalid argument.
    This may occur, for example, if some transformation type does
    not exist.
    """

    def __init__(self, message):
        """Creates an `InvalidArgumentError`."""
        super(InvalidArgumentError, self).__init__(message, INVALID_ARGUMENT)


class NotFoundError(OpError):
    """
    Raised when a requested entity (e.g., a file or directory) was not found.
    For example, if some invalid input path could raise `NotFoundError`
    if it receives the name of a file that does not exist.
    """

    def __init__(self, message, error=None):
        """Creates a `NotFoundError`."""
        super(NotFoundError, self).__init__(message, NOT_FOUND, error)

class InvalidTypeError(OpError):
    """
    Raised when a requested entity (e.g., a file or directory) was not found.
    For example, if some invalid input path could raise `NotFoundError`
    if it receives the name of a file that does not exist.
    """

    def __init__(self, message, error=None):
        """Creates a `NotFoundError`."""
        super(InvalidTypeError, self).__init__(message, NOT_FOUND, error)


class AlreadyExistsError(OpError):
    """Raised when an entity that we attempted to create already exists.
    """

    def __init__(self, op, message):
        """Creates an `AlreadyExistsError`."""
        super(AlreadyExistsError, self).__init__(message, ALREADY_EXISTS)


class OutOfRangeError(OpError):
    """Raised when an operation iterates past the valid input range.
    """

    def __init__(self, op, message):
        """Creates an `OutOfRangeError`."""
        super(OutOfRangeError, self).__init__(op, message, OUT_OF_RANGE)


class UnimplementedError(OpError):
    """Raised when an operation has not been implemented.
    Some operations may raise this error when passed otherwise-valid
    arguments that it does not currently support.
    """

    def __init__(self, op, message):
        """Creates an `UnimplementedError`."""
        super(UnimplementedError, self).__init__(op, message, UNIMPLEMENTED)