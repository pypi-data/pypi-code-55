from collections import defaultdict
from typing import List, DefaultDict

from buz.event import Subscriber
from buz.event.sync import (
    SubscriberAlreadyRegisteredException,
    SubscriberNotRegisteredException,
)
from buz.event.sync import Locator


class InstanceLocator(Locator):
    def __init__(self) -> None:
        self.__mapping: DefaultDict[str, List[Subscriber]] = defaultdict(lambda: [])

    def register(self, subscriber: Subscriber) -> None:
        event_fqn = subscriber.event_subscribed_to()
        self.__guard_subscriber_already_registered(event_fqn, subscriber)
        self.__mapping[event_fqn].append(subscriber)

    def __guard_subscriber_already_registered(self, event_fqn: str, subscriber: Subscriber) -> None:
        if subscriber in self.__mapping[event_fqn]:
            raise SubscriberAlreadyRegisteredException(subscriber)

    def unregister(self, subscriber: Subscriber) -> None:
        event_fqn = subscriber.event_subscribed_to()
        self.__guard_subscriber_not_registered(event_fqn, subscriber)
        self.__mapping[event_fqn].remove(subscriber)

    def __guard_subscriber_not_registered(self, event_fqn: str, subscriber: Subscriber) -> None:
        if subscriber not in self.__mapping[event_fqn]:
            raise SubscriberNotRegisteredException(subscriber)

    def get(self, event_fqn: str) -> List[Subscriber]:
        return self.__mapping.get(event_fqn, [])
