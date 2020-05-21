from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)  # type: ignore
class Event(ABC):
    id: str
    date: datetime

    @classmethod
    def fqn(cls) -> str:
        return f"{cls.__module__}.{cls.__name__}"
