from __future__ import annotations

from functools import wraps
from inspect import signature
from typing import Any
from typing import cast
from typing import Dict
from typing import FrozenSet
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from workflows.errors import UnhashableArgumentError


T = TypeVar("T")


class Meta(type):
    def __new__(
        mcs: Type[Meta], name: str, bases: Union[Type, Tuple[Type, ...]], namespace: Dict[str, Any],
    ) -> Meta:
        init_str = "__init__"
        try:
            init = namespace[init_str]
        except KeyError:
            pass
        else:

            @wraps(init)
            def __init__(self: Task, *args: Any, **kwargs: Any) -> None:
                try:
                    self._parameters_and_dependencies
                except AttributeError:
                    pre_attrs = set(dir(self))
                    init(self, *args, **kwargs)
                    new_attrs = set(dir(self)) - pre_attrs
                    parameters = {
                        attr for attr in new_attrs if not isinstance(getattr(self, attr), Task)
                    }
                    dependencies = {
                        attr for attr in new_attrs if isinstance(getattr(self, attr), Task)
                    }
                    self._parameters_and_dependencies = (parameters, dependencies)
                else:
                    init(self, *args, **kwargs)

            namespace[init_str] = __init__
        return super().__new__(mcs, name, bases, namespace)


_INSTANCES: Dict[Type[Task], Dict[Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]], Task]] = {}
_DEPENDENCIES: Dict[Task, Set[Task]] = {}


class Task(metaclass=Meta):
    def __new__(cls: Type[Task], *args: Any, **kwargs: Any) -> Task:
        try:
            cache = _INSTANCES[cls]
        except KeyError:
            cache = _INSTANCES[cls] = {}
        for i, arg in enumerate(args, start=1):
            cls._check_hashable(desc="Positional", detail=f"{i}={arg}", value=arg)
        for key, value in kwargs.items():
            cls._check_hashable(desc="Keyword", detail=f"{key}={value}", value=value)
        try:
            ba = signature(cls.__init__).bind(cls, *args, **kwargs)
        except TypeError:
            return super().__new__(cls)  # just to get the original error
        else:
            ba.apply_defaults()
            items = cast(FrozenSet[Tuple[str, Any]], frozenset(ba.kwargs.items()))
            cache_key = (ba.args[1:], items)
            try:
                return cache[cache_key]
            except KeyError:
                self = cache[cache_key] = super().__new__(cls)
                return self

    @classmethod
    def _check_hashable(cls: Type[Task], desc: str, detail: str, value: T) -> None:
        try:
            hash(value)
        except TypeError:
            raise UnhashableArgumentError(f"{desc} argument {detail} is not hashable") from None

    @property
    def parameters(self: Task) -> Dict[str, Any]:
        parameters, _ = self._parameters_and_dependencies
        return {param: getattr(self, param) for param in parameters}

    @property
    def dependencies(self: Task) -> Set[Task]:
        _, dependencies = self._parameters_and_dependencies
        return {getattr(self, dep) for dep in dependencies}

    def all_dependencies(self: Task) -> Set[Task]:  # dead: disable
        try:
            dependencies = _DEPENDENCIES[self]
        except KeyError:
            dependencies = _DEPENDENCIES[self] = self.dependencies
        if self in dependencies:
            raise ValueError("Circular")
        while True:
            try:
                unmapped = next(dep for dep in dependencies if dep not in _DEPENDENCIES)
            except StopIteration:
                return dependencies
            else:
                unmapped_deps = _DEPENDENCIES[unmapped] = unmapped.dependencies
                if unmapped_deps:
                    raise ValueError("Circular")
                else:
                    dependencies = dependencies | unmapped_deps
