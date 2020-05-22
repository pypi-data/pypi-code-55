"""Exceptions thrown for template processing."""

import sys


class QuietException(Exception):
    """Output only the exception name and message, no traceback."""


class InvalidTemplate(QuietException):
    """Raise this exception when the template is malformed."""


class InvalidParameter(QuietException):
    """Raise this exception when a parameter is missing a value."""


class VariableKeyError(QuietException):
    """Raise this exception when a variable key does not have a value."""


class MissingAttributeError(QuietException):
    """Raise this exception when a rule is missing attributes or evaluate()."""


# No unit tests for this, due to Python mechanics.
# https://stackoverflow.com/a/46351418
def quiet_exception_hook(kind, message, traceback):
    """Print only exception name and message if based on QuietException."""
    if QuietException in kind.__bases__:
        # Only print Error Type and Message
        print(f'{kind.__name__}: {message}')
    else:
        # Print Error Type, Message and Traceback
        sys.__excepthook__(kind, message, traceback)
