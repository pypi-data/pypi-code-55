"""Contains exceptions that are raised when errors occur with the Config class."""
from autoconfiguration.exceptions.base_error import ConfigBaseError


class ConfigNotInitializedError(ConfigBaseError):
    """Raised if the Config class was not initialized."""

    def __init__(self) -> None:
        super().__init__(
            "The Config class was not initialized! Call the init function first."
        )


class ConfigClassIsNotDataclassError(ConfigBaseError):
    """Raised if a config class is not a dataclass."""

    def __init__(self) -> None:
        super().__init__(
            "The Config class or one of its sub classes is not a dataclass!"
        )


class ConfigClassAttributeError(ConfigBaseError):
    """Raised if an attribute of a config class has no value."""

    def __init__(self, attribute: str) -> None:
        super().__init__(f"The Config class has no attribute '{attribute}'")
