import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Mapping, Iterable, Optional, Union, Generic, TYPE_CHECKING, TypeVar

import pandas as pd
from dataclasses import dataclass
from kisters.water.time_series.core.time_series import TSColumnT, TimeSeriesT

if TYPE_CHECKING:
    from kisters.water.time_series.core.time_series_store import TSStoreT
else:
    TSStoreT = TypeVar("TSStoreT")


class TimeSeriesTransaction(ABC, Generic[TSStoreT, TimeSeriesT, TSColumnT]):
    """
    This abstract class provides the API to perform backend operation into TimeSeries.

    Args:
        store: The TimeSeriesStore.

    Attributes:
        store: The TimeSeriesStore.
        _ts_create_ops: A list of MetadataOperations which create TimeSeries.
        _ts_read_ops: A list of MetadataOperations which read TimeSeries
        _metadata_read_ops: A list of MetadataOperations which read TimeSeries metadata.
        _data_read_ops: A list of DataOperations which read TimeSeries data.
        _metadata_set_value_ops: A list of MetadataOperations which update TimeSeriesMetadata.
        _data_write_ops: A list of DataOperations which write TimeSeries data.
        _metadata_del_value_ops: A list of MetadataOperations which update TimeSeriesMetadata.
        _ts_delete_ops: A list of MetadataOperations which delete TimeSeries.

    Notes:
        For developers:
            To implement this class developers must implement "only" the commit_async method,
            this method is in charge to handle all the list of operations into the specific backend.
            To prevent race conditions we recommend to commit all the transactions in the following order:
                1. _ts_create_ops
                2. _ts_read_ops
                3. _ts_filter_ops
                4. _metadata_read_ops
                5. _data_read_ops
                6. _metadata_set_value_ops
                7. _data_write_ops
                8. _metadata_del_value_ops
                9. _ts_delete_ops

    """

    @dataclass
    class DataOperation:
        """
        The DataOperation dataclass holding all the information to perform a read/write operation.

        Attributes:
            time_series: The TimeSeries.
            data_frame: The pd.DataFrame holding the TimeSeries data,
                in read operations is used to retrieve the results,
                while in write operations holds the data to write.
            start: The date from which data will be writen.
            end: The date until which data will be writen (end date included).
            t0: (ensemble only) The t0 time stamp of the ensemble member.
            dispatch_info: (ensemble only) The ensemble dispatch_info identifier.
            member: (ensemble only) The ensemble member identifier.
            kwargs: The dictionary holding the additional keyword arguments.

        """

        time_series: TimeSeriesT
        data_frame: Optional[pd.DataFrame]
        start: Optional[datetime]
        end: Optional[datetime]
        t0: datetime
        dispatch_info: str
        member: str
        kwargs: Mapping

    @dataclass
    class MetadataOperation:
        """
        The MetadataOperation dataclass holding the information for CRUD operations on TimeSeries metadata.

        Attributes:
            time_series: A TimeSeries object.
            path: The time series path.
            metadata: The TimeSeries metadata dictionary.
            columns: The TimeSeries columns.
            kwargs: Additional keyword arguments used by the backend.
        """

        time_series: Optional[TimeSeriesT]
        path: str
        metadata: Optional[Dict]
        columns: Optional[List[TSColumnT]]
        kwargs: Mapping

    @dataclass
    class FilterOperation:
        """
        The FilterOperation dataclass holding the information for a filter operation.

        Attributes:
            time_series_iterable: An iterable of TimeSeries objects.
            filter: The time series filter.
            kwargs: Additional keyword arguments used by the backend.
        """

        time_series_iterable: Optional[Iterable[TimeSeriesT]]
        filter: str
        kwargs: Mapping

    def __init__(self, store: TSStoreT):
        self._store = store
        self._ts_create_ops = []
        self._ts_read_ops = []
        self._ts_filter_ops = []
        self._metadata_read_ops = []
        self._data_read_ops = []
        self._metadata_set_value_ops = []
        self._data_write_ops = []
        self._metadata_del_value_ops = []
        self._ts_delete_ops = []

    @property
    def store(self) -> TSStoreT:
        return self._store

    def __enter__(self):
        """
        For use as a context manager.

        Returns:
            The transaction.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        For use as a context manager.

        Args:
            exc_type: The exception type.
            exc_value: The exception value.
            exc_traceback: The exception traceback.

        Returns:
            False if there was an exception (PEP 343 for details).

        """
        if not exc_type:
            self.commit()
        return False

    def create_time_series(
        self, path: str, metadata: Dict, columns: List[TSColumnT], **kwargs: Mapping
    ) -> "TimeSeriesTransaction.MetadataOperation":
        """
        Add a create_time_series MetadataOperation into the transaction manager.

        Args:
            path: The TimeSeries path.
            metadata: The TimeSeries metadata dictionary.
            columns: The list of columns of the TimeSeries.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The create MetadataOperation.
        """
        create = self.MetadataOperation(
            time_series=None, path=path, metadata=metadata, columns=columns, kwargs=kwargs
        )
        self._ts_create_ops.append(create)
        return create

    def read_time_series(self, path: str, **kwargs: Mapping) -> "TimeSeriesTransaction.MetadataOperation":
        """
        Add a read_time_series MetadataOperation into the transaction manager.

        Args:
            *path: The TimeSeries path.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The read_time_series MetadataOperation.
        """
        read = self.MetadataOperation(
            time_series=None, path=path, metadata=None, columns=None, kwargs=kwargs
        )
        self._ts_read_ops.append(read)
        return read

    def filter_time_series(
        self, ts_filter: str, **kwargs: Mapping
    ) -> "TimeSeriesTransaction.FilterOperation":
        """
        Add a read_time_series MetadataOperation into the transaction manager.

        Args:
            *ts_filter: The TimeSeries path.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The read_time_series MetadataOperation.
        """
        filter_op = self.FilterOperation(time_series_iterable=None, filter=ts_filter, kwargs=kwargs)
        self._ts_filter_ops.append(filter_op)
        return filter_op

    def read_metadata(self, path: str, **kwargs: Mapping) -> "TimeSeriesTransaction.MetadataOperation":
        """
        Add a read_metadata MetadataOperation into the transaction manager.


        This call differs with read_time_series in that it sets the return value in the
        metadata attribute and it only contains the TimeSeries metadata.

        Args:
            *path: The TimeSeries path.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The read_metadata MetadataOperation.
        """
        read = self.MetadataOperation(
            time_series=None, path=path, metadata=None, columns=None, kwargs=kwargs
        )
        self._metadata_read_ops.append(read)
        return read

    def set_metadata_value(
        self, path: str, key: str, value: Any, **kwargs
    ) -> "TimeSeriesTransaction.MetadataOperation":
        """
        Add a metadata_set_value MetadataOperation into the transaction manager.

        Args:
            path: The TimeSeries path.
            key: The metadata key.
            value: The metadata value.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The update MetadataOperation.
        """
        set_metadata = self.MetadataOperation(
            time_series=None, path=path, metadata={key: value}, columns=None, kwargs=kwargs
        )
        self._metadata_set_value_ops.append(set_metadata)
        return set_metadata

    def delete_metadata_value(
        self, path: str, key: str, **kwargs
    ) -> "TimeSeriesTransaction.MetadataOperation":
        """
        Add a metadata_del_value MetadataOperation into the transaction manager.

        Args:
            path: The TimeSeries path.
            key: The metadata key to delete.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The update MetadataOperation.
        """
        del_metadata = self.MetadataOperation(
            time_series=None, path=path, metadata={key: None}, columns=None, kwargs=kwargs
        )
        self._metadata_del_value_ops.append(del_metadata)
        return del_metadata

    def delete_time_series(self, path: str, **kwargs) -> "TimeSeriesTransaction.MetadataOperation":
        """
        Add a delete_time_series MetadataOperation into the transaction manager.

        Args:
            path: The TimeSeries path.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The delete MetadataOperation.
        """
        delete = self.MetadataOperation(
            time_series=None, path=path, metadata=None, columns=None, kwargs=kwargs
        )
        self._ts_delete_ops.append(delete)
        return delete

    def read_data_frame(
        self,
        time_series: TimeSeriesT,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ) -> "TimeSeriesTransaction.DataOperation":
        """
        Add a read_data_frame DataOperation into the transaction manager.

        Args:
            time_series: The TimeSeries.
            start: The starting date from which the data will be returned, expressed either
                as an ISO Datetime string or as a datetime object. If TimeZone is not included,
                it assumes the TimeZone of the TimeSeries.
            end: The ending date until which the data will be covered (end date included),
                expressed either as an ISO Datetime string or as a datetime object. If TimeZone
                is not included, it assumes the TimeZone of the TimeSeries.

            For ensemble time series only:
                To retrieve all data points of all dispatch_infos and members set t0, dispatch_info, member
                to None including t0, dispatch_info, member as additional columns

                To retrieve a single ensemble member:
                    t0: The t0 time stamp of the ensemble member.
                    dispatch_info: Ensemble dispatch_info identifier.
                    member: Ensemble member identifier.
            **kwargs: The additional keyword arguments which are passed to the backend.

        Returns:
            The read DataOperation
        """
        read = self.DataOperation(
            time_series=time_series,
            data_frame=None,
            start=start,
            end=end,
            t0=t0,
            dispatch_info=dispatch_info,
            member=member,
            kwargs=kwargs,
        )
        self._data_read_ops.append(read)
        return read

    def write_data_frame(
        self,
        time_series: TimeSeriesT,
        data_frame: pd.DataFrame,
        t0: datetime = None,
        dispatch_info: str = None,
        member: str = None,
        **kwargs,
    ) -> "TimeSeriesTransaction.DataOperation":
        """
        Add a write_data_frame DataOperation into the transaction manager.

        Args:
            time_series: The TimeSeries.
            data_frame: The TimeSeries data to be written in the form of a pandas DataFrame.

            For ensemble time series only, start and end will be ignored,
            writes a single ensemble member at once:
                t0: the t0 time stamp of the ensemble member.
                dispatch_info: ensemble dispatch_info identifier.
                member: ensemble member identifier.
            **kwargs: The additional keyword arguments which are passed to the backend.


        Returns:
            The write DataOperation.

        """
        write = self.DataOperation(
            time_series=time_series,
            data_frame=data_frame,
            start=None,
            end=None,
            t0=t0,
            dispatch_info=dispatch_info,
            member=member,
            kwargs=kwargs,
        )
        self._data_write_ops.append(write)
        return write

    @abstractmethod
    async def commit_async(self):
        """
        Commit asynchronously all the Operations into the backend.
        """

    def commit(self):
        """
        Commit synchronously all the Operations into the backend.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.commit_async())

    @property
    def modifies_data(self) -> bool:
        """
        True if this transaction modifies the underlying data source.
        """
        if len(self._data_write_ops) > 0:
            return True
        return False

    @property
    def modifies_metadata(self) -> bool:
        """
        True if this transaction modifies the underlying metadata source.
        """
        if len(self._ts_create_ops) > 0:
            return True
        if len(self._metadata_set_value_ops) > 0:
            return True
        if len(self._metadata_del_value_ops) > 0:
            return True
        if len(self._ts_delete_ops) > 0:
            return True
        return False
