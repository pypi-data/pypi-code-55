from __future__ import annotations

from concurrent.futures._base import Executor
from concurrent.futures._base import Future
from concurrent.futures.process import ProcessPoolExecutor
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Set

from workflows.task import Task


def run_tasks(
    tasks: Iterable[Task], *args: Any, executor: Optional[Executor] = None, **kwargs: Any,
) -> None:
    task_set = set(tasks)
    for task in tasks:
        task_set.update(task.get_dependencies(recurse=True))
    futures: Dict[Task, Future] = {}
    if executor is None:
        executor_use = ProcessPoolExecutor()
    else:
        executor_use = executor
    with executor_use as executor_cm:
        while task_set:
            completed: Set[Task] = set()
            for task in task_set:
                try:
                    future = futures[task]
                except KeyError:
                    if all(dep not in task_set for dep in task.get_dependencies(recurse=True)) and (
                        task not in futures
                    ):
                        futures[task] = executor_cm.submit(task, *args, **kwargs)
                else:
                    if future.done():
                        maybe_exception = future.exception()
                        if maybe_exception is None:
                            completed.add(task)
                        else:
                            try:
                                raise RuntimeError(
                                    f"'run_tasks' failed on the task {task} with the following exception:",
                                )
                            except RuntimeError as error:
                                raise maybe_exception from error
            task_set -= completed
