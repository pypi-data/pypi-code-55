from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from functools import lru_cache
from functools import reduce
from operator import or_
from typing import Any
from typing import cast
from typing import Dict
from typing import FrozenSet
from typing import Generic
from typing import Hashable
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar

from workflows.errors import UnhashableParameterError


T = TypeVar("T")
_INSTANCES: Dict[Type[Task], Dict[FrozenSet[Tuple[str, Hashable]], Task]] = {}


class Task(Generic[T], metaclass=ABCMeta):
    def __new__(cls: Type[Task], *args: Any, **kwargs: Any) -> Task[T]:
        try:
            cache = _INSTANCES[cls]
        except KeyError:
            cache = _INSTANCES[cls] = {}
        self: Task = super().__new__(cls)
        pre_attrs = set(dir(self))
        self.__init__(*args, **kwargs)
        new_attrs = set(dir(self)) - pre_attrs
        parameters: Dict[str, Hashable] = {
            attr: cls._check_hashable(attr, getattr(self, attr))
            for attr in new_attrs
            if not isinstance(getattr(self, attr), Task)
        }
        items = cast(FrozenSet[Tuple[str, Hashable]], frozenset(parameters.items()))
        try:
            return cache[items]
        except KeyError:
            dependencies: Set[Task] = {
                getattr(self, attr) for attr in new_attrs if isinstance(getattr(self, attr), Task)
            }
            self._parameters_and_dependencies = (parameters, dependencies)
            cache[items] = self
            return self

    @abstractmethod
    def __call__(self: Task[T]) -> T:
        raise NotImplementedError

    def get_parameters(self: Task[T]) -> Dict[str, Hashable]:  # dead: disable
        parameters, _ = self._parameters_and_dependencies
        return parameters

    @lru_cache()
    def get_dependencies(self: Task[T], *, recurse: bool = False) -> Set[Task]:
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
            return dependencies

    @classmethod
    def _check_hashable(cls: Type[Task], key: str, value: Any) -> Hashable:
        try:
            hash(value)
        except TypeError:
            raise UnhashableParameterError(
                f"Parameter {cls.__name__}.{key}={value} is not hashable",
            ) from None
        else:
            return value
