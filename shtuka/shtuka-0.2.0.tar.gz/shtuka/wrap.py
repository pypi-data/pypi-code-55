"""Functions and classes for wrappers instantiating."""

import keyword

from shtuka import core
from shtuka import utils

from typing import Any  # isort:skip


class PythonSetup(core.Setup):
    """See base class."""

    def cook(self, data: Any) -> Any:
        """See base class."""

        data = self.raw(data)  # Recooking
        if isinstance(data, list):
            return self.__cook_list(data)
        elif isinstance(data, dict):
            return self.__cook_dict(data)
        else:
            return super().cook(data)

    def __cook_list(self, data: 'list') -> core.GBaseList:
        cooked: core.GBaseList
        if self.frozen:
            cooked: sh_frozenlist = sh_frozenlist(data)  # type: ignore
            assert isinstance(cooked, core.GFrozenList)  # mypy
            super(core.GFrozenList, cooked).__init__(self, data)
        else:
            cooked: sh_list = sh_list(data)  # type: ignore
            assert isinstance(cooked, core.GList)  # mypy
            super(core.GList, cooked).__init__(self, data)

        return cooked

    def __cook_dict(self, data: 'dict') -> core.GBaseDict:
        cooked: core.GBaseDict
        if self.frozen:
            cooked: sh_frozendict = sh_frozendict(data)  # type: ignore
            assert isinstance(cooked, core.GFrozenDict)  # mypy
            super(core.GFrozenDict, cooked).__init__(self, data)
        else:
            cooked: sh_dict = sh_dict(data)  # type: ignore
            assert isinstance(cooked, core.GDict)  # mypy
            super(core.GDict, cooked).__init__(self, data)

        if self.validate:
            forbidden_attributes = utils.find_forbidden_attributes(
                data=data,
                forbidden_keys=set(dir(cooked)) | set(keyword.kwlist),
            )
            if len(forbidden_attributes):
                raise ValueError(
                    "Data dict contains forbidden attributes: "
                    f"'{forbidden_attributes}'."
                )

        return cooked


def cook(
    data: Any,
    *,
    frozen: bool = False,
    strict: bool = False,
    validate: bool = False,
) -> Any:
    """Wraps raw python object to one of shtuka wrapper.

    Args:
        data: Raw python object. Could be list or dict to be considered
            as internal shtuka tree inner node. Any other type would be
            considered a leaf (either mutable or immutable).
        frozen: True if make object immutable. Immutability copies all
            inner list/dict nodes and checks leafs hashability. Any
            further converting to raw data will return copy as well to
            prevent changing.
        strict: True if create strict shtuka wrapper. Strict one would
            not wrap leafs and produce an error for missing keys
            (either for lists or dicts). Non-strict one, otherwise,
            would wrap every leaf and output an empty node for missing
            keys.
        validate: True if validate for attribute usage. Raises an error
            if meets a dict key that cannot be accessed as attribute.
            Validation goes in lazy manner, checking only those nodes
            for which wrappers were created.

    Returns:
        High-level shtuka wrapper.

    Raises:
        TypeError: When input data doesn't comply with kwargs params.

    """

    if frozen:
        data = utils.tree_copy(raw(data))
        for parents, leaf in utils.gen_leafs(data):
            if not utils.is_hashable(leaf):
                raise TypeError(
                    f"Element {leaf} at position {parents} isn't hashable."
                )

    setup = PythonSetup(frozen, strict, validate)  # noqa
    return setup.cook(data)


raw = core.Setup.raw  # Same logic


class sh_list(core.GList):  # noqa
    """List constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args: Any, **kwargs: Any):
        """Creates a list of elements.

        Args:
            *args: Args to propagate to :obj:`list` constructor.
            **kwargs: Kwargs to propagate to :obj:`list` constructor.

        """

        setup = PythonSetup()  # noqa
        data = list(*args, **kwargs)
        super().__init__(setup, data)


class sh_frozenlist(core.GFrozenList):  # noqa
    """Frozen list constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args: Any, **kwargs: Any):
        """Creates a frozen list of elements.

        Args:
            *args: Args to propagate to :obj:`list` constructor.
            **kwargs: Kwargs to propagate to :obj:`list` constructor.

        """

        setup = PythonSetup(frozen=True)  # noqa
        data = list(*args, **kwargs)
        super().__init__(setup, data)


class sh_dict(core.GDict):  # noqa
    """Dict constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args: Any, **kwargs: Any):
        """Creates a dict of elements.

        Args:
            *args: Args to propagate to :obj:`dict` constructor.
            **kwargs: Kwargs to propagate to :obj:`dict` constructor.

        """

        setup = PythonSetup()  # noqa
        data = dict(*args, **kwargs)
        super().__init__(setup, data)


class sh_frozendict(core.GFrozenDict):  # noqa
    """Frozen dict constructor with non-strict wrapping."""

    __slots__ = ()

    def __init__(self, *args: Any, **kwargs: Any):
        """Creates a frozen dict of elements.

        Args:
            *args: Args to propagate to :obj:`dict` constructor.
            **kwargs: Kwargs to propagate to :obj:`dict` constructor.

        """

        setup = PythonSetup(frozen=True)  # noqa
        data = dict(*args, **kwargs)
        super().__init__(setup, data)


def fromkeys(cls, iterable, value=None):
    """Creates dict from keys.

    Args:
        cls: Class to create with
        iterable: Keys
        value: Value

    Returns:
        New instance with keys mapped to value

    """

    return cls({k: value for k in iterable})


setattr(sh_dict, 'fromkeys', classmethod(fromkeys))  # noqa
setattr(sh_frozendict, 'fromkeys', classmethod(fromkeys))  # noqa
