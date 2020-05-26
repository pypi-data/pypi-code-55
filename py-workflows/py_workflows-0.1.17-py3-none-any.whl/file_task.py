from __future__ import annotations

from abc import abstractmethod
from concurrent.futures._base import Future
from concurrent.futures.process import ProcessPoolExecutor
from functools import reduce
from operator import or_
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import Set
from typing import Type
from typing import TypeVar

from atomic_write_path import atomic_write_path

from workflows.errors import RunTasksError
from workflows.task import Task


T = TypeVar("T")
_DEFAULT_OVERWRITE = False


class FileTask(Task[T]):
    def __call__(self: FileTask[T], *, overwrite: bool = _DEFAULT_OVERWRITE) -> T:
        path = self.path()
        if overwrite:
            out = self.compute()
            with atomic_write_path(path, overwrite=True) as temp:
                self.write(out, temp)
            return out
        else:
            try:
                return self.read(path)
            except FileNotFoundError:
                out = self.compute()
                with atomic_write_path(path, overwrite=False) as temp:
                    self.write(out, temp)
                return out

    @abstractmethod  # noqa: U100
    def compute(self: FileTask[T]) -> T:  # noqa: U100
        raise NotImplementedError

    @abstractmethod
    def path(self: FileTask) -> Path:
        raise NotImplementedError

    @abstractmethod  # noqa: U100
    def read(self: FileTask[T], path: Path) -> T:  # noqa: U100
        raise NotImplementedError

    @abstractmethod  # noqa: U100
    def write(self: FileTask, value: T, path: Path) -> None:  # noqa: U100
        raise NotImplementedError

    @classmethod
    def run(
        cls: Type[FileTask], tasks: Iterable[FileTask], *, overwrite: bool = _DEFAULT_OVERWRITE,
    ) -> None:
        tasks: Set[FileTask] = reduce(
            or_, ({task} | task.get_dependencies(recurse=True) for task in tasks), set(),
        )
        if not overwrite:
            tasks = {task for task in tasks if not task.path().exists()}
        futures: Dict[Task, Future] = {}
        with ProcessPoolExecutor() as executor:
            while tasks:
                completed: Set[Task] = set()
                for task in tasks:
                    try:
                        future = futures[task]
                    except KeyError:
                        if all(
                            dep not in tasks for dep in task.get_dependencies(recurse=True)
                        ) and (task not in futures):
                            futures[task] = executor.submit(task, overwrite=overwrite)
                    else:
                        if future.done():
                            maybe_exception = future.exception()
                            if maybe_exception is None:
                                completed.add(task)
                            else:
                                try:
                                    raise RunTasksError(f"Task {task} failed")
                                except RunTasksError as error:
                                    raise maybe_exception from error
                tasks -= completed
