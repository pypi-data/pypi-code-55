"""Base shtuka classes."""

import abc
import functools

from shtuka import meta

from typing import (  # isort:skip
    Any,
    Union,
    Type,
    NamedTuple,
    Optional,
    TypeVar,
)


class Setup(NamedTuple):
    """Wrappers creation settings."""

    frozen: bool = False
    strict: bool = False
    validate: bool = False

    def empty(self, *args, **kwargs) -> 'GEmpty':
        """Creates empty wrapper.

        We cant merge empty as cook with no parameters since we can
        always try to cook data default value.

        Args:
            *args: Positional arguments to propagate to empty wrapper
                constructor.
            **kwargs: Key-value arguments to propagate to empty wrapper
                constructor.

        Returns:
            Empty shtuka wrapper.

        """

        return GEmpty(self, *args, **kwargs)

    def cook(self, data: Any) -> Any:
        """Wraps input data with current setup.

        Args:
            data: Data to cook. Could be anything but empty wrapper.

        Returns:
            Wrapped data

        """

        data = self.raw(data)  # Recooking
        return data if self.strict else GLeaf(self, data)

    @staticmethod
    def raw(entity: Any) -> Any:
        """Performs the reverse-`cook` operation.

        Args:
            entity: Entity to unwrap.

        Returns:
            Raw object without shtuka wrappers.

        """

        return entity.x_ if isinstance(entity, GABC) else entity


# https://github.com/python/mypy/issues/8539
@functools.total_ordering  # type: ignore
class GABC(metaclass=abc.ABCMeta):
    """General abstact shtuka wrapper."""

    __fields__: meta.Fields

    def __init_subclass__(cls: Type['GABC']) -> None:
        super().__init_subclass__()

        # Collects fields (statically) from slots.
        cls.__fields__ = meta.Fields(cls)

    __slots__ = ('_setup', '__weakref__')

    def __init__(self, setup: Setup):
        """Init base shtuka class with setup setting.

        Args:
            setup: Setup settings.

        """

        super().__init__()

        self._setup = setup

    def __getstate__(self):
        return {f: getattr(self, f, None) for f in type(self).__fields__}

    def __setstate__(self, fields):
        for k, v in fields.items():
            setattr(self, k, v)

    def __repr__(self):
        clazz = type(self)
        properties_str = ', '.join(
            '{}={}'.format(field[1:], repr(getattr(self, field, None)))
            for field in clazz.__fields__
        )
        return '{}({})'.format(clazz.__name__, properties_str)

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def pprint_(self) -> str:
        """Outputs nice visualization of internals.

        Returns:
            Str of what's going on inside

        """

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __lt__(self, other):
        pass

    @abc.abstractmethod
    def __bool__(self):
        pass

    @abc.abstractmethod
    def __getitem__(self, item: Any) -> Any:
        pass

    def __getattr__(self, item):
        if item in type(self).__fields__:
            return object.__getattribute__(self, item)
        else:
            try:
                return self.__getitem__(item)
            except KeyError as e:
                raise AttributeError(str(e))

    @abc.abstractmethod
    def __add__(self, other):
        pass

    @abc.abstractmethod
    def __radd__(self, other):
        pass

    # ------------------- Keep wrappers functions ------------------- #

    @abc.abstractmethod
    def a_(self, f: Union[str, meta.Function]) -> 'GABC':
        """Applies (non-inplace) function and outputs wrapped result.

        Args:
            f: Function to apply.

        Returns:
            Wrapped result.

        """

    def coerce_(self, f: Union[str, meta.Function]) -> 'GABC':
        """Makes a coercion with type function and empty on failing.

        Coercion is considered fail when caught exception is either
        :exc:`TypeError` or :exc:`ValueError`.

        Args:
            f: Function to do coercion with.

        Returns:
            Wrapped coercion result or empty entity.

        """

        try:
            return self.a_(f)
        except (TypeError, ValueError):
            return self._setup.empty()

    def check_(self, f: Union[str, meta.Filter] = 'is-not-none') -> 'GABC':
        """Checks wrapped element with True/False filter.

        Args:
            f: Filter function to check with.

        Returns:
            Same element on True, empty entity on False.

        """

        return self if self.f_(f) else self._setup.empty()

    # ------------------- Setup converters ------------------- #

    @abc.abstractmethod
    def frozen_(self: 'T') -> 'T':
        """Freeze wrapper and return frozen copy.

        Returns:
            Frozen copy

        """

    @abc.abstractmethod
    def unfrozen_(self: 'T') -> 'T':
        """Unfreeze wrapper and return new copy.

        Returns:
            Unfrozen copy

        """

    @abc.abstractmethod
    def strict_(self: 'T') -> Any:
        """Sticker wrapper and return new copy.

        Returns:
            Strict copy

        """

    @abc.abstractmethod
    def unstrict_(self: 'T') -> 'T':
        """Un-sticker wrapper and return new copy.

        Returns:
            Un-strict copy

        """

    @abc.abstractmethod
    def validate_(self: 'T') -> 'T':
        """Validate wrapper and return new copy.

        Returns:
            Valid copy

        """

    @abc.abstractmethod
    def unvalidate_(self: 'T') -> 'T':
        """Un-validate wrapper and return new copy.

        Returns:
            Un-valid copy

        """

    # -------------------- Finalization functions ------------------- #

    @property
    @abc.abstractmethod
    def x_(self) -> Any:
        """Extracts raw python object from shtuka wrapper.

        Returns:
            A python object inside wrapper.

        Raises:
            ValueError: If tried to convert empty entity.

        """

    def f_(self, f: Union[str, meta.Function]) -> Any:
        """Alias for applying :meth:`apply_` following by :meth:`raw_`.

        Args:
            f: Function to pass to apply.

        Returns:
            Raw unwrapped function result.

        """

        return self.unstrict_().a_(f).x_

    def as_(self, f: Union[str, meta.Function]) -> 'GABC':
        """Applies function node-wise and outputs wrapped result.

        Args:
            f: Function to apply.

        Returns:
            Wrapped result.

        """

        return self.a_(f)

    def fs_(self, f: Union[str, meta.Function]) -> Any:
        """Alias for applying :meth:`as_` following by :meth:`x_`.

        Args:
            f: Function to pass to apply.

        Returns:
            Raw unwrapped function result.

        """

        return self.as_(f).x_

    @property
    @abc.abstractmethod
    def miss_(self) -> bool:
        """Checks if shtuka wrapper contains an element.

        Returns:
            True if requested element is missing.

        """

    @property
    def blank_(self) -> bool:
        """Checks if shtuka wrapper is missing one or falsy value.

        Returns:
            True if requested element is missing or falsy.

        """

        return self.miss_ or not bool(self)

    # ---------------------- &,|,/ operations ---------------------- #

    def and_(self, default) -> Any:
        """Chooses default if not blank.

        Args:
            default: Output when element is blank.

        Returns:
            Raw element or default if not blank.

        """

        return default if not self.blank_ else self.x_

    def or_(self, default) -> Any:
        """Chooses default one if blank.

        Args:
            default: Output when element is blank.

        Returns:
            Raw element or default if blank.

        """

        return default if self.blank_ else self.x_

    def alt_(self, default) -> Any:
        """Chooses default one if missing.

        Args:
            default: Output when element is missing.

        Returns:
            Raw element or default if missing.

        """

        return default if self.miss_ else self.x_

    def __and__(self, other):
        return self.and_(other)

    def __or__(self, other):
        return self.or_(other)

    def __truediv__(self, other):
        return self.alt_(other)


T = TypeVar('T', bound=GABC)


class GEmpty(GABC, meta.FieldsSetDelMixin):
    """Class for denoting empty wrapper or missing key.

    Although class derived from set/del mixin, which forces it to
    implement getters and setter, it is still immutable by design.
    Because of that, it is also hashable.

    Any two instances of this class should be treated as equal.

    """

    __slots__ = ('_parent', '_missed_key', '_last_missed', meta.HASH_FIELD)

    def __init__(
        self,
        setup: Setup,
        parent: Optional['GABC'] = None,
        missed_key: Optional[str] = None,
    ):
        """Inits missing wrapper with setup setting.

        Args:
            setup: Setup setting.
            parent: Parent wrapper.
            missed_key: Key name that invokes missing key wrapper
                creation.

        """

        super().__init__(setup)

        self._parent = parent
        self._missed_key = missed_key

        # Forward link for GC to not delete new missing object.
        self._last_missed: Optional['GEmpty'] = None

    def __str__(self):
        raise ValueError("Cant cast missing value to string.")

    def pprint_(self) -> str:
        """See base class."""
        return '<EMPTY>'

    def __eq__(self, other):
        if isinstance(other, GEmpty):
            return True

        return False

    def __lt__(self, other):
        raise TypeError(
            f"'<' not supported between instances of "
            f"'{type(self)}' and '{type(other)}'."
        )

    def __bool__(self):
        return False

    def __getitem__(self, key):
        self._last_missed = self._setup.empty(self, key)
        return self._last_missed

    def __add__(self, other):
        raise TypeError(
            meta.type_error_msg(self, '__add__', dict(other=other))
        )

    def __radd__(self, other):
        raise TypeError(
            meta.type_error_msg(self, '__radd__', dict(other=other))
        )

    def a_(self, f: Union[str, meta.Function]) -> 'GABC':
        """See base class."""
        return self._setup.empty()

    def frozen_(self):
        """See base class."""
        return self._setup._replace(frozen=True).empty()

    def unfrozen_(self):
        """See base class."""
        return self._setup._replace(frozen=False).empty()

    def strict_(self):
        """See base class."""
        return self._setup._replace(strict=True).empty()

    def unstrict_(self):
        """See base class."""
        return self._setup._replace(strict=False).empty()

    def validate_(self):
        """See base class."""
        return self._setup._replace(validate=True).empty()

    def unvalidate_(self):
        """See base class."""
        return self._setup._replace(validate=False).empty()

    @property
    def x_(self) -> Any:
        """See base class."""
        raise ValueError("Cant get a raw object from missing wrapper.")

    @property
    def miss_(self) -> bool:
        """See base class."""
        return True

    @meta.memoize
    def __hash__(self):
        return hash(None)

    def __setitem__(self, key, value):
        final_value, current_node = {key: value}, self
        while isinstance(current_node._parent, GEmpty):
            final_value = {current_node._missed_key: final_value}
            current_node = current_node._parent

        if current_node._parent is not None:
            current_node._parent[current_node._missed_key] = final_value
            return

        raise ValueError("Cant set a value to an empty wrapper.")

    def __delitem__(self, key):
        raise ValueError("Cant del a value to an empty wrapper.")


class GEntity(GABC):
    """Base abstract class for non-empty wrappers."""

    __slots__ = ('_data',)

    def __init__(self, setup: Setup, data: Any):
        """Inits entity with setup setting and data object.

        Args:
            setup: Setting setup.
            data: Data object.

        """

        super().__init__(setup)

        self._data = data

    def __str__(self):
        return str(self._data)

    def pprint_(self) -> str:
        """See base class."""
        return str(self)

    def __eq__(self, other):
        if isinstance(other, GEntity):
            return self._data == other._data

        return self._data == other

    def __lt__(self, other):
        if isinstance(other, GEntity):
            return self._data < other._data

        return self._data < other

    def __bool__(self):
        return bool(self._data)

    def __getitem__(self, key):
        return self._setup.empty()

    @meta.iobubble
    def __add__(self, other):
        return self._data + other

    @meta.ibubble
    def __radd__(self, other):
        return other + self._data

    @meta.iobubble
    def a_(self, f: Union[str, meta.Function]) -> Any:
        """See base class."""
        return meta.func_deref(f)(self._data)  # noqa

    def frozen_(self: T) -> T:
        """See base class."""
        return self._setup._replace(frozen=True).cook(self._data)  # noqa

    def unfrozen_(self: T) -> T:
        """See base class."""
        return self._setup._replace(frozen=False).cook(self._data)  # noqa

    def strict_(self: T) -> Any:
        """See base class."""
        return self._setup._replace(strict=True).cook(self._data)  # noqa

    def unstrict_(self: T) -> T:
        """See base class."""
        return self._setup._replace(strict=False).cook(self._data)  # noqa

    def validate_(self: T) -> T:
        """See base class."""
        return self._setup._replace(validate=True).cook(self._data)  # noqa

    def unvalidate_(self: T) -> T:
        """See base class."""
        return self._setup._replace(validate=False).cook(self._data)  # noqa

    @property
    def x_(self) -> Any:
        """See base class."""
        return self._data

    @property
    def miss_(self) -> bool:
        """See base class."""
        return False


class GLeaf(GEntity):
    """Single non-composite object wrapper."""

    __slots__ = (meta.HASH_FIELD,)

    @meta.memoize
    def __hash__(self):
        return hash(self._data)
