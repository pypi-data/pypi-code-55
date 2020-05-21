from abc import ABC, abstractmethod

from buz.event import Event


class Subscriber(ABC):
    @staticmethod
    @abstractmethod
    def event_subscribed_to() -> str:
        pass

    @abstractmethod
    def consume(self, event: Event) -> None:
        pass
