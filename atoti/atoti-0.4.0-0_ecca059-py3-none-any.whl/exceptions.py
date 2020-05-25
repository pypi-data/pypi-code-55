"""Custom atoti exceptions.

The custom exceptions are here to disguise the "ugly" stack traces which occur when Py4J raises
a Java error.
If any other exception is raised by the code inside the custom hook, it is processed normally.

This module is public so the exceptions classes are public and can be documented.
"""

from __future__ import annotations

import sys
import traceback
from functools import wraps
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Optional, Tuple, Type, Union

from ._ipython_utils import run_from_ipython
from .vendor.atotipy4j.protocol import Py4JError, Py4JJavaError, Py4JNetworkError

if TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.ultratb import AutoFormattedTB


class AtotiException(Exception):
    """The generic atoti exception class.

    All exceptions which inherit from this class will be treated differently when raised.
    However, this exception is still handled by the default excepthook.
    """


class AtotiJavaException(AtotiException):
    """Exception thrown when Py4J throws a Java exception."""

    def __init__(
        self, message: str, java_traceback: str, java_exception: Py4JJavaError  # type: ignore
    ):
        """Create a new AtotiJavaException.

        Args:
            message: The exception message.
            java_traceback: The stack trace of the Java exception, used to build
                the custom stack trace for atoti.
            java_exception: The exception from the Java code returned by Py4J.
        """
        # Call the base constructor with the parameters it needs
        super().__init__(message)
        self.java_traceback = java_traceback
        self.java_exception = java_exception


class AtotimNetworkException(AtotiException):
    """Exception thrown when Py4J throws a network exception."""


class AtotiPy4JException(AtotiException):
    """Exception thrown when Py4J throws a Py4JError."""


class NoCubeStartedException(Exception):
    """Exception thrown when an action requires a cube to be strated but it is not."""


def _atoti_hook(kind: Type[Any], value: Exception, trace_back: TracebackType):
    """Handle custom exceptions differently.

    This function applies our custom excepthook to any AtotiException which is raised. We pass
    any other type of exception on to the default excepthook to be treated normally.

    Args:
        kind: The type of the exception which is being raised.
        value: The exception being raised.
        trace_back: The current stack trace.
    """
    # If the exception is one of the kinds we want to handle differently, we indicate it here
    if AtotiException in kind.__bases__:
        # Print original traceback
        traceback.print_tb(tb=trace_back)
        sys.stderr.write(f"{value.__class__.__name__}: {value} \n")
        if kind == AtotiJavaException and isinstance(value, AtotiJavaException):
            # In the case of a Java exception, we append the Java stack trace
            # to the python trace back
            sys.stderr.write(value.java_traceback + "\n")
    else:
        # Call the default excepthook for any other kind of exception
        sys.__excepthook__(kind, value, trace_back)


def _get_exc_info(
    exc_tuple: Optional[Tuple[type, Exception, traceback.TracebackException]] = None
) -> Tuple[
    Union[Type[BaseException], type],
    Optional[Union[BaseException, Exception]],
    Optional[Union[TracebackType, traceback.TracebackException]],
]:
    """Extract exception info.

    This methods tries to provide an exc_tuple in all cases. If the tuple it is called with is null,
    we try to extract the information from the system info.

    Args:
        exc_tuple: Tuple containing the three following elements:
            - etype: The type of the exception being raised
            - value: The exception being raised
            - traceback: The current traceback

    Returns:
        The exc_tuple if it exists.

    """
    if exc_tuple is None:
        etype, value, trace_back = sys.exc_info()
    else:
        etype, value, trace_back = exc_tuple

    if etype is None:
        raise ValueError("No exception to find.")

    return etype, value, trace_back


def _atoti_exception_handler(
    shell: InteractiveShell,  # type: ignore
    etype: type,
    evalue: Exception,
    trace_back: traceback.TracebackException,
    tb_offset: Optional[int] = None,
):
    """Handle exceptions in IPython Notebooks.

    We need this call to the handler to tell the IPython kernel to use our custom traceback
    function.

    Args:
        shell: The IPython InteractiveShell
        etype: The type of the exception being raised
        evalue: The exception being raised
        trace_back: The current traceback
        tb_offset: The offset to display the traceback with

    """
    shell.showtraceback((etype, evalue, trace_back), tb_offset=tb_offset)


def _atoti_traceback_function(
    traceback_printer: AutoFormattedTB,  # type: ignore
    func: Callable,
):
    """Wrap IPython showtraceback method."""
    # Declare wrapper
    @wraps(func)
    def showtraceback(*args: Any, **kwargs: Any):
        if len(args) > 1:
            try:
                _, value, _ = _get_exc_info(args[1])
            except ValueError:
                value = None  # avoid unbound type error
                sys.stderr.write("No exception to print, returning...")

            if isinstance(value, AtotiException):
                # the function has been called from our custom handler in this case
                # We want to reformat the stack trace
                traceback_lines = traceback.format_exception(*sys.exc_info())
                # traceback_lines = [traceback_lines[0]] + traceback_lines[-2:]
                stb = traceback_printer.structured_traceback(tb=traceback_lines)
                stb = traceback_printer.stb2text(stb)
                sys.stderr.write(stb)
                if isinstance(value, AtotiJavaException):
                    # If the error comes from Java, we append the Java stack_trace
                    # to the python one
                    sys.stderr.write(value.java_traceback)
            else:
                # Return regalar std-err for other exceptions
                func(*args, **kwargs)
        else:
            # Return regular std-err for normal exceptions
            func(*args, **kwargs)

    return showtraceback


def _setup_atoti_exception_handling():
    """Set up custom exception handling for Py4J related errors."""
    if run_from_ipython():
        from IPython.core.getipython import get_ipython

        # pylint: disable=redefined-outer-name
        from IPython.core.interactiveshell import InteractiveShell
        from IPython.core.ultratb import AutoFormattedTB

        # pylint: enable=redefined-outer-name

        # IPython won't let us override the excepthook, so we define custom handlers
        get_ipython().set_custom_exc((AtotiException,), _atoti_exception_handler)

        traceback_printer = AutoFormattedTB(mode="Plain", tb_offset=1)

        # Monkey patch the showtraceback method
        InteractiveShell.showtraceback = _atoti_traceback_function(
            traceback_printer, InteractiveShell.showtraceback
        )
    else:
        # If we are running with a regular python kernel, we override the excepthook
        sys.excepthook = _atoti_hook


def _java_api_call_wrapper(method: Callable):
    """Wrap calls to the Java API to handle Py4J and Java exceptions."""
    # Declare wrapper
    @wraps(method)
    def catch_py4j_exceptions(*args: Any, **kwargs: Any) -> Any:
        try:
            return method(*args, **kwargs)
        except Py4JJavaError as java_exception:
            raise AtotiJavaException(
                "An error occurred in the JVM:", str(java_exception), java_exception
            )
        except Py4JNetworkError as error:
            raise AtotimNetworkException(str(error))
        except Py4JError as error:
            raise AtotiPy4JException(str(error))

    return catch_py4j_exceptions
