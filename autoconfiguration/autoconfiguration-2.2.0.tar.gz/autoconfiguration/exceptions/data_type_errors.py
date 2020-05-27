"""
Contains exceptions that are raised when errors occur while trying to convert
configuration values to the specified types.
"""
from typing import Type, Any

from autoconfiguration.exceptions.base_error import ConfigBaseError


class UnableToConvertConfigValueToTypeError(ConfigBaseError):
    """Raised if configuration value could not be converted to its expected type."""

    def __init__(self, value: str, expected_type: Type[Any]):
        super().__init__(
            f"The value '{value}' could not be converted to the expected type '"
            f"{expected_type}'!"
        )
