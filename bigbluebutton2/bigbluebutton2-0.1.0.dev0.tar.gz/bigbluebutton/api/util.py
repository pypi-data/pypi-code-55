from typing import Any

from inflection import camelize, underscore


def snake_to_camel(snake: str) -> str:
    """Convert PEP-8 complicant snake case name to special lower camel case.

    >>> snake_to_camel("test_string")
    'testString'
    >>> snake_to_camel("meeting_id")
    'meetingID'
    """
    all_caps = ("Url", "Pw", "Id")

    camel = camelize(snake, False)
    for word in all_caps:
        camel = camel.replace(word, word.upper())

    return camel


def camel_to_snake(camel: str) -> str:
    """Convert camel or lower camel case name to PEP-8 compliant snake case used in our classes.

    >>> camel_to_snake("meetingID")
    'meeting_id'
    """
    return underscore(camel)


def get_target_type(cls: type, attr: str) -> type:
    """Guess the type of a field in a class by looking at its type annotation.

    It either returns the type hint itself, or the first type argument if
    it is a composite (e.g. int for a typing.Union[int, float] or a
    typing.Optional[int].

    WARNING: This is not generic code, but tailored to the use cases in the
    specific data classes in this code base.
    """
    type_ = cls.__annotations__[attr]

    if hasattr(type_, "__args__"):
        type_ = type_.__args__[0]

    return type_


def to_field_type(cls: type, attr: str, value: str) -> Any:
    """Convert a string value to a type fitting the type of a field by looking at its type hint."""
    type_ = get_target_type(cls, attr)

    if type_ is bool:
        if value.lower() in ("true", "yes", "on", "1"):
            return True
        elif value.lower() in ("false", "no", "off", "0"):
            return False
        else:
            return ValueError(f"String {value} can not be coerced into a boolean.")
    else:
        return type_(value)
