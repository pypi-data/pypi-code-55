import asyncio

from hero import ExtensionConfig, version
from hero.utils import AsyncUsingDB, SyncToAsync, SyncToAsyncThreadSafe


__version__ = 'v0.1.0-beta'

VERSION = version(__version__)


class SchedulerConfig(ExtensionConfig):
    verbose_name = "Scheduler"


def schedulable(func):
    """Marks a controller method as schedulable."""
    if not asyncio.iscoroutinefunction(func) or isinstance(func, (AsyncUsingDB, SyncToAsync, SyncToAsyncThreadSafe)):
        raise TypeError('Schedulable controller method must be async.')

    func.schedulable = True
    return func
