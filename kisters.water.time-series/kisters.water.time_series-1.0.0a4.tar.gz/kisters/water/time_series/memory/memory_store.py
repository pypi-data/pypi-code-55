from typing import TypeVar, TYPE_CHECKING

from kisters.water.time_series.core.time_series_store import TimeSeriesStore
from kisters.water.time_series.memory.memory_time_series_transaction import (
    MemoryTimeSeriesTransaction,
)
if TYPE_CHECKING:
    from kisters.water.time_series.core.time_series import TSColumnT
    from kisters.water.time_series.memory.memory_time_series import MemoryTimeSeriesT
else:
    MemoryTimeSeriesT = TypeVar("MemoryTimeSeriesT")
    TSColumnT = TypeVar("TSColumnT")


class MemoryStore(TimeSeriesStore[MemoryTimeSeriesT, TSColumnT]):
    """FileStore provides a TimeSeriesStore for in memory data

    Args:

    Examples:
        .. code-block:: python

            from kisters.water.time_series.file_io import MemoryStore
            fs = MemoryStore()
            ts = fs.get_by_path('validation/inner_consistency1/station1/H')
    """

    def __init__(self):
        self._time_series = {}

    def transaction(self) -> MemoryTimeSeriesTransaction:
        return MemoryTimeSeriesTransaction(self)


MemoryStoreT = TypeVar("MemoryStoreT", bound=MemoryStore)
