from typing import TypeVar

from kisters.water.time_series.memory import MemoryTimeSeries


class ParquetTimeSeries(MemoryTimeSeries):
    """ParquetTimeSeries"""


ParquetTimeSeriesT = TypeVar("ParquetTimeSeriesT", bound=ParquetTimeSeries)
