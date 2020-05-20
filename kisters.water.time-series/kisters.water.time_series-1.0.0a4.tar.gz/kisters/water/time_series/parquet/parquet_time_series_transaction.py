from typing import TYPE_CHECKING, TypeVar

from kisters.water.time_series.core.time_series import TSColumnT
from kisters.water.time_series.memory.memory_time_series_transaction import MemoryTimeSeriesTransaction

if TYPE_CHECKING:
    from kisters.water.time_series.parquet.parquet_store import ParquetStoreT
    from kisters.water.time_series.parquet.parquet_time_series import ParquetTimeSeriesT
else:
    ParquetStoreT = TypeVar("ParquetStoreT")
    ParquetTimeSeriesT = TypeVar("ParquetTimeSeriesT")


class ParquetTimeSeriesTransaction(
    MemoryTimeSeriesTransaction[ParquetStoreT, ParquetTimeSeriesT, TSColumnT]
):
    def commit(self) -> None:
        super().commit()

        # Sync to parquet file
        if self.modifies_data or self.modifies_metadata:
            self.store._save_table()
