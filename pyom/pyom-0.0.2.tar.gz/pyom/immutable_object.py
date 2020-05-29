from typing import Any, TypeVar

ImmutableObjectType = TypeVar('ImmutableObjectType', bound='ImmutableObject')


class ImmutableObject:
    def with_props(  # type: ignore[misc] # Explicit "Any" is not allowed # noqa: F821
        self: ImmutableObjectType,
        **kwargs: Any,
    ) -> ImmutableObjectType:
        params = {**self.__dict__}

        for k, v in kwargs.items():
            params[k] = v

        return self.__class__(**params)  # type: ignore[call-arg] # Too many arguments for "ImmutableObject" # noqa: F821
