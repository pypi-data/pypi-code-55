"""Composite shtuka classes."""

import abc
from collections import abc as collections_abc

import yaml

from shtuka import meta
from shtuka import utils
from shtuka.core import base

from typing import Union, Any  # isort:skip


class GComposite(
    base.GEntity, collections_abc.Container, metaclass=abc.ABCMeta
):
    """Wrapper for inner composite node."""

    __slots__ = ()

    def pprint_(self) -> str:
        """See base class."""
        return yaml.dump(self._data)

    def _contains(self, key: Any) -> bool:
        """Checks if node has particular key.

        This is not the same as '__contains__' dunder method, since
        some composite structures (like 'list') define contains for
        values, rather then for keys.

        Args:
            key: Key to check

        Returns:
            True if node has input key.

        """

        return key in self

    @meta.ibubble
    def __getitem__(self, key: Any) -> Any:
        setup = self._setup

        if self._contains(key):
            return setup.cook(self._data[key])
        elif setup.strict:
            raise KeyError(f"No such key: '{key}'.")
        else:
            return setup.empty(self, key)


class GBaseList(GComposite, meta.SequenceMixin):
    """List base."""

    __slots__ = ()

    def _contains(self, key: Any) -> bool:
        if isinstance(key, int):
            if not len(self):
                return False

            if key < 0:
                key = key % len(self)

            return 0 <= key < len(self)
        elif isinstance(key, slice):
            return True
        else:
            return False

    def __getitem__(self, key: Any) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError as e:
            if isinstance(key, int):
                # Correct error for list indexing
                raise IndexError(key)
            else:
                raise e

    @meta.iobubble
    def as_(self, f: Union[str, meta.Function]) -> 'GBaseList':
        """See base class."""
        # noinspection PyTypeChecker
        return [c.fs_(f) for c in self.unstrict_()]  # type: ignore

    @meta.iobubble
    def __mul__(self, n: int) -> 'GBaseList':
        return self._data * n

    __rmul__ = __mul__


class GBaseDict(GComposite, meta.MappingMixin):
    """Dict base."""

    __slots__ = ()

    @meta.iobubble
    def __add__(self, other):
        if isinstance(other, dict):
            return utils.merge(self._data, other)

        return super().__add__(other)

    @meta.ibubble
    def __radd__(self, other):
        if isinstance(other, dict):
            return utils.merge(other, self._data)

        return super().__radd__(other)

    @meta.iobubble
    def as_(self, f: Union[str, meta.Function]) -> 'GBaseDict':
        """See base class."""
        items = self.unstrict_().items()
        # noinspection PyTypeChecker
        return {k: v.fs_(f) for k, v in items}  # type: ignore

    def get(self, k, default):  # noqa
        return self.unstrict_()[k].or_(default)


class GFrozenList(GBaseList):
    """Immutable List."""

    __slots__ = (meta.HASH_FIELD,)

    @meta.memoize
    def __hash__(self):
        return hash(tuple(self))


class GFrozenDict(GBaseDict):
    """Immutable Dict."""

    __slots__ = (meta.HASH_FIELD,)

    @meta.memoize
    def __hash__(self):
        return hash(tuple(self.items()))


class GList(
    GBaseList, meta.FieldsSetDelMixin, collections_abc.MutableSequence,
):
    """Mutable list."""

    __slots__ = ()

    @meta.ibubble
    def __setitem__(self, key, value):
        self._data[key] = value

    @meta.ibubble
    def __delitem__(self, key):
        del self._data[key]

    @meta.ibubble
    def __iadd__(self, other):
        self._data += other
        return self

    @meta.ibubble
    def __imul__(self, other):
        self._data *= other
        return self

    @meta.ibubble
    def insert(self, index, value):
        """See base class."""
        self._data.insert(index, value)

    @meta.obubble
    def copy(self):
        """Copies a wrapper.

        Returns:
            Copy of new wrapper.

        """

        return self._data.copy()

    @meta.ibubble
    def sort(self, *args, **kwargs):
        """Sorts list.

        Args:
            *args: Args to propagate to list.sort method.
            **kwargs: Kwargs to propagate to list.sort method.

        """

        self._data.sort(*args, **kwargs)


class GDict(
    GBaseDict, meta.FieldsSetDelMixin, collections_abc.MutableMapping,
):
    """Mutable dict."""

    __slots__ = ()

    @meta.ibubble
    def __setitem__(self, key, value):
        self._data[key] = value

    @meta.ibubble
    def __delitem__(self, key):
        del self._data[key]

    @meta.ibubble
    def __iadd__(self, other):
        self._data = utils.merge(self._data, other, inplace=True)
        return self

    @meta.obubble
    def copy(self):
        """Copies a wrapper.

        Returns:
            Copy of new wrapper.

        """

        return self._data.copy()

    def setdefault(self, k, default):  # noqa
        if k in self:
            return self[k]

        self[k] = default

        return default
