from typing import Collection

from buz.event import Subscriber


class Locator:
    def get(self, event_fqn: str) -> Collection[Subscriber]:
        pass
