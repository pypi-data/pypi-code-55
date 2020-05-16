from abc import ABC, abstractmethod
from inspect import signature
import datetime as dt
from dataclasses import dataclass
from typing import Any, Optional
from mario.util import Status


@dataclass()
class FnConfig:
    fn: str
    name: str
    args: Any
    description: Optional[str] = None


class DoFn(ABC):
    __signature__ = NotImplemented

    def __init_subclass__(cls, **kwargs):
        cls.__signature__ = signature(cls.run)

    def __init__(self, name: str):
        self.name = name
        self.kwargs = None
        self.errors = []
        self.__result__ = None
        self.runs = 0
        self.time_started = None
        self.time_ended = None
        self.status = Status.NOT_STARTED

    def collect_output(self):
        stage_output = {
            "step": self.__class__.__name__,
            "name": self.name,
            "status": self.status,
            "errors": self.errors,
            "times_run": self.runs,
            "time_started": self.time_started.isoformat() if self.time_started else None,
            "time_ended": self.time_ended.isoformat() if self.time_ended else None,
            "duration": (self.time_ended - self.time_started).total_seconds() if self.time_ended else None,
        }
        return stage_output

    def attach_args(self, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def run(self, *args, **kwargs):
        return NotImplemented

    def __call__(self, **kwargs):
        try:
            self.attach_args(**kwargs)
            self.time_started = dt.datetime.utcnow()
            self.__result__ = self.run(**self.kwargs)
            self.status = Status.SUCCEESS
        except Exception as err:
            self.errors.append(err.__str__())
            self.status = Status.FAIL
            raise
        finally:
            self.time_ended = dt.datetime.utcnow()
            self.runs += 1
        return self.status

