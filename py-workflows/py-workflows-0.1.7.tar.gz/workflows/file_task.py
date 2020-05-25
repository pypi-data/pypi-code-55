from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from atomic_write_path import atomic_write_path

from workflows.task import Task
from workflows.task import TaskMeta


T = TypeVar("T")


class FileTaskMeta(TaskMeta):
    def __new__(
        mcs: Type[FileTaskMeta],
        name: str,
        bases: Union[Type, Tuple[Type, ...]],
        namespace: Dict[str, Any],
    ) -> Type[FileTask]:
        call_str = "__call__"
        try:
            call = namespace[call_str]
        except KeyError:
            pass
        else:

            def __call__(self: FileTask[T], *, overwrite: bool = False) -> T:
                if overwrite:
                    out = call(self, overwrite=True)
                    with atomic_write_path(self.path, overwrite=True) as temp:
                        self.write(out, temp)
                    return out
                else:
                    try:
                        return self.read(self.path)
                    except FileNotFoundError:
                        out = call(self, overwrite=False)
                        with atomic_write_path(self.path, overwrite=False) as temp:
                            self.write(out, temp)
                        return out

            namespace[call_str] = __call__

        return super().__new__(mcs, name, bases, namespace)


class FileTask(Task[T], metaclass=FileTaskMeta):
    @abstractmethod  # noqa: U100
    def __call__(self: FileTask[T], *, overwrite: bool = False) -> T:  # noqa: U100
        raise NotImplementedError

    @property
    @abstractmethod
    def path(self: FileTask) -> Union[Path, str]:
        raise NotImplementedError

    @abstractmethod  # noqa: U100
    def read(self: FileTask[T], path: Union[Path, str]) -> T:  # noqa: U100
        raise NotImplementedError

    @abstractmethod  # noqa: U100
    def write(self: FileTask, value: T, path: Union[Path, str]) -> None:  # noqa: U100
        raise NotImplementedError
