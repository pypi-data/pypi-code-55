import abc

from macrobase_driver.context import Context
from macrobase_driver.config import CommonConfig, AppConfig, DriverConfig


class Endpoint(object, metaclass=abc.ABCMeta):
    """
    Endpoint protocol for processing from macrobase and his drivers
    """

    def __init__(self, context: Context, config: CommonConfig[AppConfig, DriverConfig], *args):
        self.context = context
        self._config = config
        self.__name__ = self.__class__.__name__

    @property
    def config(self) -> CommonConfig[AppConfig, DriverConfig]:
        return self._config

    async def __call__(self, *args, **kwargs):
        return await self.handle(*args, **kwargs)

    @abc.abstractmethod
    async def handle(self, *args, **kwargs):
        raise NotImplementedError
