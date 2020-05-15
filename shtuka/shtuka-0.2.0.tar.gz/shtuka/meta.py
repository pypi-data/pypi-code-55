"""Python class building helpers and utilities."""

import abc
import collections
from collections import abc as collections_abc
import functools
import itertools
import operator
import types

from typing import Callable, Any, Union, Tuple, Optional  # isort:skip

HASH_FIELD = '_hash'

Filter = Callable[[Any], bool]
# Filter is subtype of Function. There is no option in python typing to
# maintain covariant subtyping, so this is bypass solution.
Function = Union[Filter, Callable[[Any], Any]]

_NAME_TO_FUNC = (
    ('is-none', functools.partial(operator.is_, None)),
    ('is-not-none', functools.partial(operator.is_not, None)),
)


def func_deref(f: Union[str, Function]) -> Function:
    """Dereferences function by str name.

    Args:
        f: Either str name to deref or function itself.

    Returns:
        Function.

    """

    if isinstance(f, str):
        return dict(_NAME_TO_FUNC)[f]

    return f


class Fields(collections.UserList):
    """Slots fields list abstraction."""

    def __init__(self, cls: Any):
        """Inits fields collection with class slots in mro order.

        Args:
            cls: Class to fetch fields from.

        """

        fields = list(
            itertools.chain.from_iterable(
                getattr(c, '__slots__', ()) for c in cls.__mro__
            )
        )
        assert len(set(fields)) == len(fields)

        if '_data' in fields:
            fields.remove('_data')
            fields = ['_data'] + fields

        fields.remove('__weakref__')

        super().__init__(fields)

        self._set = set(fields)

    def __contains__(self, item: object) -> bool:
        """Checks field existence by name.

        Args:
            item: Field name to check.

        Returns:
            True if there is such field name.

        """

        return item in self._set


def memoize(field: Union[str, Callable] = HASH_FIELD):
    """Method memoization with fields name arg.

    Args:
        field: Field name or function to use.

    Returns:
        Memoize function wrapper.

    """

    def memoize_wrapper(f: Callable, inner_field=field):
        """Method memoization.

        Args:
            f: Method to memoize.
            inner_field: Fields to use.

        Returns:
            New function with memoization logic.

        """

        @functools.wraps(f)
        def f_wrapper(self, *args, **kwargs):
            """Wraps f with single invocation hashing."""

            if getattr(self, inner_field, None) is None:
                setattr(self, inner_field, f(self, *args, **kwargs))

            return getattr(self, inner_field)

        return f_wrapper

    if isinstance(field, str):
        return memoize_wrapper
    else:
        return memoize_wrapper(field, HASH_FIELD)


def type_error_msg(self, f, kwargs) -> str:
    """Raises type error for method invocation.

    Args:
        self: Object
        f: Method
        kwargs: Arguments

    Returns:
        Type error message

    """

    kwargs_str = ', '.join(
        f'{k} of type {type(v).__name__}' for k, v in kwargs.items()
    )
    return (
        f"Cant {f} with {type(self).__name__} and " f"arguments: {kwargs_str}."
    )


def _bubble(
    name0: Optional[Union[str, Callable[..., Any]]] = None,
    *names1: str,
    output: bool = True,
):
    """Method bubbling.

    Args:
        name0: Either function to wrap or first name to wrap
        names1: Successive names to wrap
        output: True if wrap output.

    Returns:
        Bubbling function wrapper

    """

    def bubble_wrapper(f: Callable, names: Optional[Tuple[str, ...]]):
        """Function bubbling."""

        @functools.wraps(f)
        def f_wrapper(self, *args, **kwargs):
            """Wraps f with bubbling."""

            setup = self._setup

            try:
                kwargs.update(zip(f.__code__.co_varnames[1:], args))  # noqa
                for name in names if names is not None else kwargs.keys():
                    value = kwargs[name]

                    if isinstance(value, slice):
                        value = slice(
                            setup.raw(value.start),
                            setup.raw(value.stop),
                            setup.raw(value.step),
                        )

                    kwargs[name] = setup.raw(value)
            except ValueError:
                raise TypeError(type_error_msg(self, f.__name__, kwargs))

            result = f(self, **kwargs)

            if output:
                result = setup.cook(result)

            return result

        return f_wrapper

    if isinstance(name0, types.FunctionType):  # No arguments
        return bubble_wrapper(name0, names=None)
    else:
        return functools.partial(
            bubble_wrapper, names=None if name0 is None else (name0,) + names1
        )


ibubble = functools.partial(_bubble, output=False)
obubble = _bubble()
iobubble = functools.partial(_bubble, output=True)


class FieldsSetDelMixin(metaclass=abc.ABCMeta):
    """Add attributes set/del manipulation along with class fields."""

    __fields__: Fields
    __slots__ = ()

    @abc.abstractmethod
    def __setitem__(self, key: Any, value: Any) -> None:
        """Sets value at key."""

    def __setattr__(self, key, value):
        if key in type(self).__fields__:
            return object.__setattr__(self, key, value)
        else:
            return self.__setitem__(key, value)

    @abc.abstractmethod
    def __delitem__(self, key: Any) -> None:
        """Deletes value at key."""

    def __delattr__(self, key):
        return self.__delitem__(key)


# noinspection PyUnresolvedReferences
class SequenceMixin(collections_abc.Sequence, metaclass=abc.ABCMeta):
    """Sequence mixin for inner data."""

    __slots__ = ()
    _data: Any

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for i in range(len(self._data)):
            yield self[i]

    @ibubble
    def __contains__(self, value):
        return value in self._data


# noinspection PyUnresolvedReferences
class MappingMixin(collections_abc.Mapping, metaclass=abc.ABCMeta):
    """Mapping mixin for inner data."""

    __slots__ = ()
    _data: Any

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    @ibubble
    def __contains__(self, key):
        return key in self._data
