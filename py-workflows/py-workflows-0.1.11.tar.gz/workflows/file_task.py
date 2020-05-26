from __future__ import annotations

from abc import abstractmethod
from concurrent.futures._base import Executor
from concurrent.futures._base import Future
from concurrent.futures.process import ProcessPoolExecutor
from functools import reduce
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from atomic_write_path import atomic_write_path

from workflows.errors import RunTasksError
from workflows.task import Task


T = TypeVar("T")


class FileTask(Task[T]):
    def __call__(self: FileTask[T], *, overwrite: bool = True) -> T:
        if overwrite:
            out = self.compute()
            with atomic_write_path(self.path(), overwrite=True) as temp:
                self.write(out, temp)
            return out
        else:
            try:
                return self.read(self.path())
            except FileNotFoundError:
                out = self.compute()
                with atomic_write_path(self.path(), overwrite=False) as temp:
                    self.write(out, temp)
                return out

    @abstractmethod  # noqa: U100
    def compute(self: FileTask[T]) -> T:  # noqa: U100
        raise NotImplementedError

    @abstractmethod
    def path(self: FileTask) -> Union[Path, str]:
        raise NotImplementedError

    @abstractmethod  # noqa: U100
    def read(self: FileTask[T], path: Union[Path, str]) -> T:  # noqa: U100
        raise NotImplementedError

    @abstractmethod  # noqa: U100
    def write(self: FileTask, value: T, path: Union[Path, str]) -> None:  # noqa: U100
        raise NotImplementedError

    @classmethod
    def run(
        cls: Type[FileTask],
        tasks: Iterable[FileTask],
        *,
        executor: Optional[Executor] = None,
        overwrite: bool = False,
    ) -> None:
        tasks: Set[FileTask] = reduce(
            lambda x, y: x | {y} | y.get_dependencies(recurse=True), tasks, set(),
        )
        if not overwrite:
            tasks = {task for task in tasks if not Path(task.path()).exists()}
        futures: Dict[Task, Future] = {}
        if executor is None:
            executor_use = ProcessPoolExecutor()
        else:
            executor_use = executor
        with executor_use as executor_cm:
            while tasks:
                completed: Set[Task] = set()
                for task in tasks:
                    try:
                        future = futures[task]
                    except KeyError:
                        if all(
                            dep not in tasks for dep in task.get_dependencies(recurse=True)
                        ) and (task not in futures):
                            futures[task] = executor_cm.submit(task, overwrite=overwrite)
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
