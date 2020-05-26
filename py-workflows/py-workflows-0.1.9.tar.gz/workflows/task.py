from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from functools import lru_cache
from functools import reduce
from functools import wraps
from operator import or_
from typing import Any
from typing import cast
from typing import Dict
from typing import FrozenSet
from typing import Generic
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from workflows.errors import UnhashableParameterError

T = TypeVar("T")
_INSTANCES: Dict[Type[Task], Dict[Tuple[Tuple[Any, ...], FrozenSet[Tuple[str, Any]]], Task]] = {}


class TaskMeta(ABCMeta):
    def __new__(
        mcs: Type[TaskMeta],
        name: str,
        bases: Union[Type, Tuple[Type, ...]],
        namespace: Dict[str, Any],
    ) -> Type[Task]:
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
            for key, value in self.get_parameters().items():
                self._check_hashable(key, value)

        if init is None:
            namespace[init_str] = __init__
        else:
            namespace[init_str] = wraps(init)(__init__)
        return super().__new__(mcs, name, bases, namespace)


class Task(Generic[T], metaclass=TaskMeta):
    def __new__(cls: Type[Task], *args: Any, **kwargs: Any) -> Task[T]:
        try:
            cache = _INSTANCES[cls]
        except KeyError:
            cache = _INSTANCES[cls] = {}
        self: Task = super().__new__(cls)
        self.__init__(*args, **kwargs)
        items = cast(FrozenSet[Tuple[str, Any]], frozenset(self.get_parameters().items()))
        try:
            return cache[items]
        except KeyError:
            cache[items] = self
            return self

    @abstractmethod
    def __call__(self: Task[T]) -> T:
        raise NotImplementedError

    def get_parameters(self: Task[T]) -> Dict[str, Any]:
        parameters, _ = self._parameters_and_dependencies
        return {param: getattr(self, param) for param in parameters}

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
            return {getattr(self, dep) for dep in dependencies}

    @classmethod
    def _check_hashable(cls: Type[Task], key: str, value: Any) -> None:
        try:
            hash(value)
        except TypeError:
            raise UnhashableParameterError(
                f"Parameter {cls.__name__}.{key}={value} is not hashable",
            ) from None
