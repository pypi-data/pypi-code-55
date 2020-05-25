"""Common error types."""

from typing import Optional, cast

import attr
from typing_extensions import final

from . import exception_formatter, pretty_printer
from .exception_formatter import ErrorDisplayStrategy
from .types import DeserializableType, Primitive, TerramareError


@attr.s(auto_attribs=True, frozen=True)
class BaseDeserializationError(Exception):
    """Base exception raised when a deserializer fails."""

    value: Primitive
    target_t: DeserializableType
    cause: Optional[exception_formatter.Cause[Exception]] = None
    msg: Optional[str] = None
    display_strategy: ErrorDisplayStrategy = ErrorDisplayStrategy.DEFAULT

    @final
    def _get_msg(self) -> str:
        """Return a string description of the error."""
        if self.msg is not None:
            return self.msg
        return "cannot read value '{}' into '{}'".format(
            pretty_printer.print_primitive(self.value),
            pretty_printer.print_type_name(self.target_t),
        )

    @final
    def __str__(self) -> str:
        """Format the exception message."""

        def get_metadata(
            e: Exception,
        ) -> exception_formatter.ExceptionData[Exception, Exception]:
            if isinstance(e, BaseDeserializationError):
                return exception_formatter.ExceptionData(
                    e,
                    e.cause if e.cause is not None else {},
                    e._get_msg(),  # pylint: disable=protected-access
                    e.display_strategy,
                )
            return exception_formatter.ExceptionData(
                e, {}, str(e), ErrorDisplayStrategy.DEFAULT
            )

        return exception_formatter.format_exception(cast(Exception, self), get_metadata)


class DeserializationError(BaseDeserializationError, TerramareError):
    """External-facing exception raised when deserialization fails."""


class InternalDeserializationError(BaseDeserializationError):
    """Raised when a deserializer fails. Caught internally."""


@attr.s(auto_attribs=True, frozen=True)
class BaseDeserializerFactoryError(Exception):
    """Base exception raised when deserializer creation fails."""

    target_t: DeserializableType
    msg: str
    cause: Optional[exception_formatter.Cause[Exception]] = None
    display_strategy: ErrorDisplayStrategy = ErrorDisplayStrategy.DEFAULT

    @final
    @staticmethod
    def cannot_create_msg(deserializer_desc: str) -> str:
        """Format the message for standard deserializer creation failure."""
        return "cannot create {} deserializer".format(deserializer_desc)

    @final
    def __str__(self) -> str:
        """Format the exception message."""

        def get_metadata(
            e: Exception,
        ) -> exception_formatter.ExceptionData[Exception, Exception]:
            if isinstance(e, BaseDeserializerFactoryError):
                return exception_formatter.ExceptionData(
                    e,
                    e.cause if e.cause is not None else {},
                    e.msg,
                    e.display_strategy,
                )
            return exception_formatter.ExceptionData(
                e, {}, str(e), ErrorDisplayStrategy.DEFAULT
            )

        return exception_formatter.format_exception(cast(Exception, self), get_metadata)


class DeserializerFactoryError(BaseDeserializerFactoryError, TerramareError):
    """Externally-facing exception raised when deserializer creation fails."""


class InternalDeserializerFactoryError(BaseDeserializerFactoryError):
    """Raised when deserializer creation fails. Caught internally."""
