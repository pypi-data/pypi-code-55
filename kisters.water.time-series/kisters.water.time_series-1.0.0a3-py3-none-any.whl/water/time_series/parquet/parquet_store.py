import json
import os
from typing import TypeVar

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from kisters.water.time_series.core.time_series import EnsembleMemberInfo
from kisters.water.time_series.core.time_series_store import TSColumnT
from kisters.water.time_series.memory.memory_store import MemoryStore
from kisters.water.time_series.parquet.parquet_time_series import ParquetTimeSeries, ParquetTimeSeriesT
from kisters.water.time_series.parquet.parquet_time_series_transaction import ParquetTimeSeriesTransaction


class ParquetStore(MemoryStore[ParquetTimeSeriesT, TSColumnT]):
    """ParquetStore provides a TimeSeriesStore for time series stored in Parquet files.

    Args:
        filename: The path to the Parquet file used for storage.

    Examples:
        .. code-block:: python

            from kisters.water.time_series.parquet import ParquetStore
            ts_store = ParquetStore("test.pq")
            ts = ts_store.get_by_path("validation/inner_consistency1/station1/H")
    """

    path_column = "tsPath"
    t0_column = "t0"
    member_column = "member"
    dispatch_info_column = "dispatchInfo"
    time_stamp_column = "index"

    index_columns = [path_column, t0_column, member_column, dispatch_info_column, time_stamp_column]
    categorical_columns = [path_column, t0_column, member_column, dispatch_info_column]

    metadata_metadata_field = b"tsMetadata"

    def __init__(self, filename: str):
        super().__init__()

        self._filename = filename
        if not os.path.isabs(self._filename):
            self._filename = os.path.abspath(self._filename)

        if os.path.isfile(self._filename):
            self._load_table()

    def _load_table(self) -> None:
        # Load Parquet file
        master_table = pq.read_table(self._filename)

        # Extract metadata
        master_metadata = json.loads(master_table.schema.metadata[self.metadata_metadata_field])
        for path, metadata in master_metadata.items():
            self._time_series[path] = ParquetTimeSeries(self, path, metadata, {})

        # Convert to pandas
        master_df = master_table.to_pandas(self_destruct=True)
        del master_table

        # Set index
        master_df.set_index(
            self.index_columns, inplace=True,
        )

        # Partition into traces
        for (path, t0, member, dispatch_info), group in master_df.groupby(
            level=[self.path_column, self.t0_column, self.member_column, self.dispatch_info_column]
        ):
            df_ts = (
                group.reset_index().drop(columns=self.categorical_columns).set_index(self.time_stamp_column)
            )

            self._time_series[path]._data[
                EnsembleMemberInfo(pd.to_datetime(t0), dispatch_info, member)
            ] = df_ts

    def _save_table(self) -> None:
        """Save to Parquet file."""

        # Build master data frame
        data_frames = []
        metadata = {}
        for ts in self._time_series.values():
            metadata[ts.path] = ts.metadata._metadata
            for member_info, df in ts._data.items():
                df_copy = df.reset_index()
                df_copy.insert(0, self.path_column, ts.path)
                df_copy.insert(
                    1, self.t0_column, str(pd.to_datetime(member_info.t0))
                )  # Don't use a datetime column here as it triggers some undesirable magic inside pandas.
                df_copy.insert(2, self.member_column, member_info.member)
                df_copy.insert(3, self.dispatch_info_column, member_info.dispatch_info)
                data_frames.append(df_copy)
        if len(data_frames) > 0:
            master_df = pd.concat(data_frames)
        else:
            master_df = pd.DataFrame(data={index_column: [] for index_column in self.index_columns})
        for column in self.categorical_columns:
            master_df[column] = master_df[column].astype("category")  # Save memory

        # Convert master data frame to arrow table
        table = pa.Table.from_pandas(master_df, preserve_index=False)

        # Add metadata
        table = table.replace_schema_metadata(
            {**table.schema.metadata, self.metadata_metadata_field: json.dumps(metadata)}
        )

        # Save
        pq.write_table(table, self._filename)

    def transaction(self) -> ParquetTimeSeriesTransaction:
        return ParquetTimeSeriesTransaction(self)


ParquetStoreT = TypeVar("ParquetStoreT", bound=ParquetStore)
