from __future__ import annotations

import datetime as dt
from abc import abstractmethod
from concurrent.futures._base import Future
from concurrent.futures.process import ProcessPoolExecutor
from dataclasses import dataclass
from functools import reduce
from operator import or_
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Type
from typing import TypeVar
from typing import Union

from atomic_write_path import atomic_write_path
from dateutil.rrule import rrule
from dateutil.tz import EPOCH
from dateutil.tz import gettz
from dateutil.tz import UTC

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


def floor_datetime(
    freq: int,
    *,
    as_of: Union[dt.datetime, Callable[..., dt.datetime]] = lambda: dt.datetime.now(tz=UTC),
    interval: int = 1,
    wkst: Optional[int] = None,
    bysetpos: Optional[Union[int, Sequence[int]]] = None,
    bymonth: Optional[Union[int, Sequence[int]]] = None,
    bymonthday: Optional[Union[int, Sequence[int]]] = None,
    byyearday: Optional[Union[int, Sequence[int]]] = None,
    byeaster: Optional[Union[int, Sequence[int]]] = None,
    byweekno: Optional[Union[int, Sequence[int]]] = None,
    byweekday: Optional[Union[int, Sequence[int]]] = None,
    byhour: Optional[Union[int, Sequence[int]]] = None,
    byminute: Optional[Union[int, Sequence[int]]] = None,
    bysecond: Optional[Union[int, Sequence[int]]] = None,
    tz: Union[str, dt.tzinfo] = UTC,
) -> dt.datetime:
    try:
        as_of_use = as_of()
    except TypeError:
        as_of_use = as_of
    epoch_utc = EPOCH.replace(tzinfo=UTC)
    if as_of_use < epoch_utc:
        raise ValueError(f"{as_of_use} is before the Epoch ({epoch_utc})")

    @dataclass
    class Period:
        start: dt.datetime
        end: dt.datetime
        scale: int

    def get_period() -> Period:
        start, scale = epoch_utc, 1
        while True:
            _, end = rrule(
                freq,
                dtstart=start,
                interval=scale * interval,
                wkst=wkst,
                count=2,
                bysetpos=bysetpos,
                bymonth=bymonth,
                bymonthday=bymonthday,
                byyearday=byyearday,
                byeaster=byeaster,
                byweekno=byweekno,
                byweekday=byweekday,
                byhour=byhour,
                byminute=byminute,
                bysecond=bysecond,
            )
            if start <= as_of_use <= end:
                return Period(start, end, scale)
            else:
                start, scale = end, 2 * scale

    period = get_period()

    def bisect_period(period: Period) -> dt.datetime:
        if period.scale == 1:
            if period.start <= as_of_use < period.end:
                return period.start
            else:
                return period.end
        else:
            half_scale, _ = divmod(period.scale, 2)
            _, mid, _ = rrule(
                freq,
                dtstart=period.start,
                interval=half_scale * interval,
                wkst=wkst,
                count=3,
                bysetpos=bysetpos,
                bymonth=bymonth,
                bymonthday=bymonthday,
                byyearday=byyearday,
                byeaster=byeaster,
                byweekno=byweekno,
                byweekday=byweekday,
                byhour=byhour,
                byminute=byminute,
                bysecond=bysecond,
            )
            if period.start <= as_of_use <= mid:
                start, end = period.start, mid
            else:
                start, end = mid, period.end
            return bisect_period(Period(start, end, half_scale))

    result = bisect_period(period)
    try:
        tz_use = gettz(tz)
    except TypeError:
        tz_use = tz
    return result.astimezone(tz_use)
