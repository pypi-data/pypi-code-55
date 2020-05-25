from __future__ import annotations

from functools import reduce
from functools import wraps
from inspect import signature
from operator import or_
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
_INSTANCES: Dict[Type[Task], Dict[Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]], Task]] = {}


class Meta(type):
    def __new__(
        mcs: Type[Meta], name: str, bases: Union[Type, Tuple[Type, ...]], namespace: Dict[str, Any],
    ) -> Meta:
        init_str = "__init__"
        try:
            init = namespace[init_str]
        except KeyError:

            init = None

            def call_init(self: Task, *args: Any, **kwargs: Any) -> None:
                super(Task, self).__init__(*args, **kwargs)

        else:

            def call_init(self: Task, *args: Any, **kwargs: Any) -> None:
                init(self, *args, **kwargs)

        def __init__(self: Task, *args: Any, **kwargs: Any) -> None:
            try:
                self._parameters_and_dependencies
            except AttributeError:
                pre_attrs = set(dir(self))
                call_init(self, *args, **kwargs)
                new_attrs = set(dir(self)) - pre_attrs
                parameters = {
                    attr for attr in new_attrs if not isinstance(getattr(self, attr), Task)
                }
                dependencies = {attr for attr in new_attrs if isinstance(getattr(self, attr), Task)}
                self._parameters_and_dependencies = (parameters, dependencies)
            else:
                call_init(self, *args, **kwargs)

        if init is None:
            namespace[init_str] = __init__
        else:
            namespace[init_str] = wraps(init)(__init__)
        return super().__new__(mcs, name, bases, namespace)


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

    def __init__(self: Task) -> None:
        pass

    @classmethod
    def _check_hashable(cls: Type[Task], desc: str, detail: str, value: T) -> None:
        try:
            hash(value)
        except TypeError:
            raise UnhashableArgumentError(f"{desc} argument {detail} is not hashable") from None

    def get_parameters(self: Task) -> Dict[str, Any]:  # dead: disable
        parameters, _ = self._parameters_and_dependencies
        return {param: getattr(self, param) for param in parameters}

    def get_dependencies(self: Task, *, recurse: bool = False) -> Set[Task]:
        if recurse:
            dependencies = self.get_dependencies(recurse=False)
            while True:
                expanded = reduce(
                    or_, (dep.get_dependencies(recurse=False) for dep in dependencies), set(),
                )
                if expanded.issubset(dependencies):
                    return dependencies
                else:
                    dependencies = dependencies | expanded
        else:
            _, dependencies = self._parameters_and_dependencies
            return {getattr(self, dep) for dep in dependencies}
