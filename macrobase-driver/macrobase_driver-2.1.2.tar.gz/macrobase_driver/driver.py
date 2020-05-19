from abc import ABCMeta, abstractmethod
from asyncio import AbstractEventLoop, get_event_loop, new_event_loop, set_event_loop
from typing import List, Dict

from macrobase_driver.context import Context
from macrobase_driver.config import DriverConfig, CommonConfig, AppConfig
from macrobase_driver.hook import HookHandler


class MacrobaseDriver(object, metaclass=ABCMeta):

    def __init__(self, config: CommonConfig[AppConfig, DriverConfig], name: str = None, loop: AbstractEventLoop = None, *args, **kwargs):
        self.name = name
        self._loop = loop

        self._hooks: Dict[str, List[HookHandler]] = {}
        self._config = config
        self.context = Context()

    def __repr__(self):
        return f'<{type(self)} name:{self.name}>'

    @property
    @abstractmethod
    def config(self) -> CommonConfig[AppConfig, DriverConfig]:
        pass

    @property
    def loop(self) -> AbstractEventLoop:
        if self._loop is None:
            self._loop = new_event_loop()
            set_event_loop(self._loop)

        return self._loop

    @abstractmethod
    def add_hook(self, name: str, handler):
        if name not in self._hooks:
            self._hooks[name] = []

        self._hooks[name].append(HookHandler(self, handler))

    async def _call_hooks(self, name: str):
        if name not in self._hooks:
            return

        for handler in self._hooks[name]:
            await handler(self, self.loop)

    def run(self, *args, **kwargs):
        pass
