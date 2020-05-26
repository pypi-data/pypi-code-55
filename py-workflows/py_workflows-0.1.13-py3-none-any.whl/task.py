from __future__ import annotations

from abc import ABCMeta
from abc import abstractmethod
from functools import lru_cache
from functools import wraps
from typing import Any
from typing import cast
from typing import Dict
from typing import Generic
from typing import Hashable
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from functional_itertools import CDict
from functional_itertools import CSet

from workflows.errors import UnhashableParameterError


T = TypeVar("T")


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
            pass
        else:

            @wraps(init)
            def __init__(self: Task, *args: Any, **kwargs: Any) -> None:
                try:
                    self._parameters_and_dependencies
                except AttributeError:
                    pre_attrs = CSet(dir(self))
                    init(self, *args, **kwargs)
                    new_attrs: CDict[str, Any] = CSet(set(dir(self)) - pre_attrs).filter(
                        lambda x: x != "_parameters_and_dependencies",
                    ).map_dict(lambda x: getattr(self, x))
                    parameters: CDict[str, Hashable] = new_attrs.filter_keys(
                        lambda x: x != "_parameters_and_dependencies",
                    ).filter_values(lambda x: not isinstance(x, Task)).map_items(
                        lambda k, v: (k, self._check_hashable(k, v)),
                    )
                    dependencies: CSet[Task] = new_attrs.values().set().filter(
                        lambda x: isinstance(x, Task),
                    )
                    self._parameters_and_dependencies = (parameters, dependencies)
                else:
                    init(self, *args, **kwargs)
                for key, value in self.get_parameters().items():
                    self._check_hashable(key, value)

            namespace[init_str] = __init__
        return cast(Type["Task"], super().__new__(mcs, name, bases, namespace))


class Task(Generic[T], metaclass=TaskMeta):
    @abstractmethod
    def __call__(self: Task[T]) -> T:
        raise NotImplementedError

    def __eq__(self: Task[T], other: Task[T]) -> bool:
        return (
            isinstance(self, type(other))
            and isinstance(other, type(self))
            and self.get_parameters() == other.get_parameters()
        )

    def __hash__(self: Task[T]) -> int:
        return hash(frozenset(self.get_parameters().items()))

    def get_parameters(self: Task[T]) -> CDict[str, Hashable]:
        try:
            parameters, _ = self._parameters_and_dependencies
        except AttributeError:
            return CDict()
        else:
            return parameters

    @lru_cache()
    def get_dependencies(self: Task[T], *, recurse: bool = False) -> CSet[Task]:
        if recurse:
            dependencies = self.get_dependencies(recurse=False)
            while True:
                expanded = dependencies.reduce(
                    lambda x, y: x.chain([y]).chain(y.get_dependencies(recurse=False)),
                    initial=CSet(),
                )
                if expanded.issubset(dependencies):
                    return dependencies
                else:
                    dependencies = CSet(dependencies | expanded)
        else:
            try:
                _, dependencies = self._parameters_and_dependencies
            except AttributeError:
                return CSet()
            else:
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
