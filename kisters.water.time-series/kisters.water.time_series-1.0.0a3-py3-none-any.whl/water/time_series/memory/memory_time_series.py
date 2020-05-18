from datetime import datetime
from typing import Any, Dict, TYPE_CHECKING, List, TypeVar

import pandas as pd

from kisters.water.time_series.core import TimeSeries, TimeSeriesMetadata
from kisters.water.time_series.core.time_series import EnsembleMemberInfo, TSColumnT

if TYPE_CHECKING:
    from kisters.water.time_series.memory.memory_store import MemoryStoreT
else:
    MemoryStoreT = TypeVar("MemoryStoreT")


class MemoryTimeSeries(TimeSeries[MemoryStoreT, TSColumnT]):
    def __init__(
        self,
        store: MemoryStoreT,
        path: str,
        metadata: Dict[str, Any],
        data: Dict[EnsembleMemberInfo, pd.DataFrame],
    ):
        """
        Create a TimeSeries object directly with the metadata and data given.

        Args:
            store: Parent TimeSeriesStore object.
            path: Time series path.
            metadata: Mapping with all the metadata of the TimeSeries.
            data: Dict of DataFrame objects containing TimeSeries data.
        """
        super().__init__(store)
        self._path = path
        self._metadata = TimeSeriesMetadata(self, metadata)
        self._data = data

    @property
    def path(self) -> str:
        return self._path

    @property
    def metadata(self) -> TimeSeriesMetadata:
        return self._metadata

    def coverage_from(self, t0: datetime = None, dispatch_info: str = None, member: str = None) -> datetime:
        return self._data[EnsembleMemberInfo(t0, dispatch_info, member)].index[0]

    def coverage_until(self, t0: datetime = None, dispatch_info: str = None, member: str = None) -> datetime:
        return self._data[EnsembleMemberInfo(t0, dispatch_info, member)].index[-1]

    def ensemble_members(self, t0_start: datetime = None, t0_end: datetime = None) -> List[EnsembleMemberInfo]:
        return list(self._data.keys())


MemoryTimeSeriesT = TypeVar("MemoryTimeSeriesT")
