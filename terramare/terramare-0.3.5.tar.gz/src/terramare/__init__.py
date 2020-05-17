"""Automatically deserialize complex objects from simple Python types."""

from .errors import DeserializationError, DeserializerFactoryError  # noqa: F401
from .terramare import deserialize_into  # noqa: F401
