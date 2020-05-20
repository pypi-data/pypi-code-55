# pylint: disable=W0143
"""Client implementation using SQL database

Supported databases: sqlite, postgresql
"""

import copy
import functools
import inspect
import multiprocessing as mp
import typing
import uuid

import sqlalchemy as sqla

from .. import deid, errors
from .. import models as M
from .. import schemas as T
from .. import utils
from ..config import IngestConfig, StrategyConfig
from . import db_transactions
from .abstract import Client


S = typing.TypeVar("S")  # pylint: disable=C0103

# do not create lock instance in import time otherwise
# we will get leaked semaphores warnings in child processes
# when using spawn multiprocessing start method (default on windows)
sqlite_lock = None  # pylint: disable=C0103


def set_lock(lock) -> None:
    """
    Set lock object, used to have the same lock object
    in all processes even if using spawn process start method.
    """
    global sqlite_lock  # pylint: disable=W0603,C0103
    sqlite_lock = lock


class DBClient(Client):  # pylint: disable=R0904
    """Ingest DB client implementing crud interface"""

    def __init__(self, url: str):
        super().__init__(url)
        self.engine, self.sessionmaker = utils.init_sqla(url)

        if self.engine.name == "sqlite":
            if not sqlite_lock:
                set_lock(mp.Lock())
            with sqlite_lock:
                M.Base.metadata.create_all(self.engine)

    def __getattr__(self, name):
        method_name = None
        for prefix in ("get_all", "get", "update", "find_one", "count_all", "batch_writer"):
            if name.startswith(prefix):
                method_name = prefix
                break

        if method_name in ("get_all", "get", "update", "find_one", "count_all"):
            model_name = name.replace(method_name, "").strip("_")
            model_name = "".join([part.capitalize() for part in model_name.split("_")])
            func = getattr(self, method_name)
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                return func(model_name, *args, **kwargs)
            return _wrapper
        if method_name == "batch_writer":
            type_, model_name = name.replace(method_name, "").strip("_").split("_", maxsplit=1)
            model_name = "".join([part.capitalize() for part in model_name.split("_")])
            func = getattr(self, method_name)
            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                return func(type_, model_name, *args, **kwargs)
            return _wrapper
        raise AttributeError(f"Unknown attribute: {name}")

    def check_connection(self):
        """Check whether or not the connection works"""
        try:
            # Test query
            self.engine.execute(sqla.text('SELECT 1'))
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    def call_db(self, func: typing.Callable[..., S], *args, **kwargs) -> S:
        """Run the specified function in a transaction"""
        # pylint: disable=E1101
        session = self.sessionmaker()
        if session.bind.name == "sqlite":
            sqlite_lock.acquire()
        try:
            result = func(session, *args, **kwargs)
            session.commit()
        except:
            session.rollback()
            raise
        else:
            return result
        finally:
            session.close()
            if session.bind.name == "sqlite":
                sqlite_lock.release()

    # Non-ingest-bound methods

    def create_ingest(
        self,
        config: IngestConfig,
        strategy_config: StrategyConfig,
        fw_auth: typing.Optional[T.FWAuth] = None
    ) -> T.IngestOutAPI:
        if not fw_auth:
            fw_auth = utils.get_fw_auth(utils.get_api_key())
        ingest = M.Ingest(
            api_key=fw_auth.api_key,
            fw_host=fw_auth.host,
            fw_user=fw_auth.user,
            config=config.dict(exclude_none=True),
            strategy_config=strategy_config.dict(exclude_none=True),
            # TODO: user provided label from config
        )
        ingest_out = self.call_db(db_transactions.add, ingest)
        self.bind(ingest_out.id)  # type: ignore
        return T.IngestOutAPI(**ingest_out.dict())

    def list_ingests(self) -> typing.Iterable[T.IngestOutAPI]:
        query = sqla.orm.Query(M.Ingest)
        return self._iter_query(query, [M.Ingest.created], T.IngestOutAPI)

    def next_task(self, worker: str) -> typing.Optional[T.TaskOut]:
        """Get next pending task, assign to given worker and set status running"""
        return self.call_db(db_transactions.next_task, worker)

    def delete_ingest(self, ingest_id: uuid.UUID) -> None:
        ingest = self.call_db(db_transactions.get, M.Ingest, ingest_id)
        ingest = T.IngestOutAPI(**ingest.dict())
        if not T.IngestStatus.is_terminal(ingest.status):
            raise errors.IngestIsNotDeletable(f"Ingest status ({str(ingest.status)}) is not terminal")

        # in case of abort for example the running tasks are not terminated
        if self.call_db(db_transactions.has_running_tasks, self.ingest_id):
            raise errors.IngestIsNotDeletable("Ingest has running tasks")

        self.call_db(db_transactions.delete_ingest, ingest_id)

    # Ingest-bound methods

    @property
    def ingest(self) -> T.IngestOutAPI:
        """Get ingest operation the client bind to"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    def load_subject_csv(self, subject_csv: typing.BinaryIO) -> None:
        """Load subject CSV file"""
        self.call_db(db_transactions.load_subject_csv, self.ingest_id, subject_csv)

    def start(self) -> T.IngestOutAPI:
        """Start ingest scanning"""
        ingest = self.call_db(db_transactions.start, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    def review(self, changes=None) -> T.IngestOutAPI:
        """Review (accept) ingest, add any changes and start importing"""
        ingest = self.call_db(db_transactions.review, self.ingest_id, changes)
        return T.IngestOutAPI(**ingest.dict())

    def abort(self) -> T.IngestOutAPI:
        """Abort ingest operation"""
        ingest = self.call_db(db_transactions.abort, self.ingest_id)
        return T.IngestOutAPI(**ingest.dict())

    @property
    def progress(self) -> T.Progress:
        """Get ingest scan task and item/file/byte counts by status"""
        return self.call_db(db_transactions.get_progress, self.ingest_id)

    @property
    def summary(self) -> T.Summary:
        """Get ingest hierarchy node and file count by level and type"""
        return self.call_db(db_transactions.get_summary, self.ingest_id)

    @property
    def report(self) -> T.Report:
        """Get ingest status, elapsed time per status and list of failed tasks"""
        return self.call_db(db_transactions.get_report, self.ingest_id)

    @property
    def tree(self) -> typing.Iterable[T.ContainerOut]:
        """Yield hierarchy nodes (containers)"""
        query = (
            sqla.orm.Query([
                M.Container.id,
                M.Container.level,
                M.Container.path,
                M.Container.parent_id,
                M.Container.src_context,
                M.Container.dst_context,
                M.Container.ingest_id,
                sqla.sql.func.count(M.Item.id).label("files_cnt"),
                sqla.sql.func.sum(M.Item.bytes_sum).label("bytes_sum"),
            ])
            .outerjoin(M.Container.items)  # pylint: disable=E1101
            .filter(M.Container.ingest_id == self.ingest_id)
            .group_by(M.Container.id)
        )
        return self._iter_query(query, [M.Container.path], T.ContainerOut)

    @property
    def audit_logs(self) -> typing.Iterable[str]:
        """Yield audit log CSV lines"""
        query = (
            sqla.orm.Query([
                M.Item.id,
                M.Item.dir,
                M.Item.filename,
                M.Item.existing,
                M.Item.skipped,
                M.Container.dst_path,
                M.Task.status,
                M.Error.code.label("error_code"),
                M.Error.message.label("error_message"),
            ])
            .outerjoin(M.Item.container, M.Item.task, M.Item.errors)  # pylint: disable=E1101
            .filter(M.Item.ingest_id == self.ingest_id)
        )
        filepath_errors = (
            sqla.orm.Query([
                M.Error.id,
                M.Error.code,
                M.Error.message,
                M.Error.filepath,
            ])
            .filter(
                M.Error.ingest_id == self.ingest_id,
                M.Error.filepath.isnot(None),
            )
        )

        fields = ["src_path", "dst_path", "status", "existing", "error_code", "error_message"]
        first = True
        for item in self._iter_query(query, [M.Item.dir], T.AuditLogOut):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            # TODO normalize src path, make sure win32/local works
            values = dict(
                src_path=f"{self.ingest.config.src_fs}{item.dir}/{item.filename}",
                dst_path=f"{item.dst_path}/{item.filename}",
                status="skipped" if item.skipped else item.status.name,
                existing=item.existing,
            )
            if item.error_code:
                error = errors.get_error_by_code(item.error_code)
                values["error_code"] = error.code
                values["error_message"] = item.error_message or error.message
            elif item.status == T.TaskStatus.failed:
                values["error_code"] = errors.BaseIngestError.code
                values["error_message"] = errors.BaseIngestError.message
            row = ",".join(_csv_field_str(values.get(field)) for field in fields)
            yield f"{row}\n"

        for filepath_error in self._iter_query(filepath_errors, [M.Error.created], T.Error):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            values = dict(
                src_path=f"{self.ingest.config.src_fs}/{filepath_error.filepath}",
                status="skipped",
                error_code=filepath_error.code,
                error_message=filepath_error.message,
            )
            row = ",".join(_csv_field_str(values.get(field)) for field in fields)
            yield f"{row}\n"

    @property
    def deid_logs(self) -> typing.Iterable[str]:
        """Yield de-id log CSV lines"""
        ingest = self.ingest
        assert ingest.config.de_identify

        # add fields from all deid file profiles
        fields = ["src_path", "type"]
        profile_name = ingest.config.deid_profile
        profiles = ingest.config.deid_profiles
        deid_profile = deid.load_deid_profile(profile_name, profiles)
        for file_profile in deid_profile.file_profiles:
            fields.extend(file_profile.get_log_fields())

        query = (
            sqla.orm.Query(M.DeidLog)
            .filter(M.DeidLog.ingest_id == self.ingest_id)
        )
        first = True
        for deid_log in self._iter_query(query, [M.DeidLog.created], T.DeidLogOut):
            if first:
                first = False
                header = ",".join(fields)
                yield f"{header}\n"

            before = {"src_path": deid_log.src_path, "type": "before", **deid_log.tags_before}
            before_row = ",".join(_csv_field_str(before.get(field)) for field in fields)
            yield f"{before_row}\n"

            after = {"src_path": deid_log.src_path, "type": "after", **deid_log.tags_after}
            after_row = ",".join(_csv_field_str(after.get(field)) for field in fields)
            yield f"{after_row}\n"

    @property
    def subjects(self) -> typing.Iterable[str]:
        """Yield subject CSV lines"""
        subject_config = self.ingest.config.subject_config
        if not subject_config:
            return
        query = (
            sqla.orm.Query(M.Subject)
            .filter(M.Subject.ingest_id == self.ingest_id)
        )
        first = True
        for subject in self._iter_query(query, [M.Subject.code], T.SubjectOut):
            if first:
                first = False
                fields = [subject_config.code_format] + subject_config.map_keys
                header = ",".join(fields)
                yield f"{header}\n"
            values = [subject.code] + subject.map_values
            row = ",".join(_csv_field_str(value) for value in values)
            yield f"{row}\n"

    # Ingest-bound extra methods

    @property
    def api_key(self) -> str:
        """Get the associated api key of the ingest"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        return ingest.api_key  # type: ignore

    def add(self, schema: T.Schema) -> T.Schema:
        """Add new task/container/item/deid-log to the ingest"""
        model_name = type(schema).__name__.replace("In", "")
        assert model_name in ("Task", "Container", "Item", "Error", "DeidLog")
        model_cls = getattr(M, model_name)
        model = model_cls(ingest_id=self.ingest_id, **schema.dict())
        return self.call_db(db_transactions.add, model)

    def get(self, model_name: str, model_id: uuid.UUID) -> T.Schema:
        """Get a task/container/item/deid-log by id"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        return self.call_db(db_transactions.get, model_cls, model_id)

    def get_all(self, model_name: str, *conditions: typing.Any) -> typing.Iterable[T.Schema]:
        """Get all ingests/tasks/containers/items/deid-logs by filters"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        order_by = _get_paginate_order_by_col(model_cls)
        query = sqla.orm.Query(model_cls).filter(model_cls.ingest_id == self.ingest_id)
        for condition in conditions:
            query = query.filter(condition)
        return self._iter_query(query, [order_by], model_cls.schema_cls())

    def get_items_sorted_by_dst_path(self) -> typing.Iterable[T.ItemWithContainerPath]:
        """Get items sorted by destination path including the filename.

        Primarily used in the detect duplicates task where sorting makes possible to
        find filepath conflicts without holding too much information in memory
        or overload the db backend with too much queries.
        """
        query = (
            sqla.orm.Query([
                M.Item.id,
                M.Item.dir,
                M.Item.filename,
                M.Item.existing,
                M.Container.path.label("container_path"),
            ])
            .join(M.Item.container)
            .filter(M.Item.ingest_id == self.ingest_id)
        )
        return self._iter_query(
            query,
            [M.Container.path.label("container_path"), M.Item.filename],
            T.ItemWithContainerPath,
        )

    def get_items_with_error_count(self) -> typing.Iterable[T.ItemWithErrorCount]:
        """Get all items with the number of realated errors"""
        query = (
            sqla.orm.Query([
                M.Item.id,
                M.Item.existing,
                sqla.sql.func.count(M.Error.id).label("error_cnt"),
            ])
            .outerjoin(M.Item.errors)  # pylint: disable=E1101
            .group_by(M.Item.id)
            .filter(M.Item.ingest_id == self.ingest_id)
        )

        return self._iter_query(query, [M.Item.id], T.ItemWithErrorCount)

    def count_all(self, model_name: str) -> int:
        """Get count of tasks/containers/items/deid-logs"""
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        model_cls = getattr(M, model_name)
        return self.call_db(db_transactions.count_all, self.ingest.id, model_cls)

    def update(self, model_name: str, model_id: uuid.UUID, **updates: typing.Any) -> T.Schema:
        """Update a task/container/item"""
        assert model_name in ("Task", "Container", "Item")
        model_cls = getattr(M, model_name)
        return self.call_db(db_transactions.update, model_cls, model_id, **updates)

    def find_one(self, model_name: str, *conditions: typing.Any) -> typing.Any:
        """
        Get a task/container/item/deid-log by the specified key.

        Conditions need to specified in a way that uniquely identify an item.
        """
        assert model_name in ("Task", "Container", "Item", "DeidLog")
        assert conditions
        model_cls = getattr(M, model_name)
        conditions = (model_cls.ingest_id == self.ingest_id,) + conditions
        return self.call_db(db_transactions.find_one, model_cls, *conditions)

    def bulk(self, type_: str, model_name: str, mappings: typing.List[dict]) -> None:
        """Bulk add/update tasks/containers/items"""
        assert type_ in ("insert", "update")
        assert model_name in ("Task", "Container", "Item", "Error")
        model_cls = getattr(M, model_name)
        if type_ == "insert":
            def _set_ingest_id(obj):
                obj = copy.copy(obj)
                obj["ingest_id"] = self.ingest_id
                return obj
            mappings = [_set_ingest_id(m) for m in mappings]
        self.call_db(db_transactions.bulk, type_, model_cls, mappings)

    def start_resolving(self) -> T.IngestOut:
        """Set ingest status to resolving and add resolve task if all scans finished"""
        ingest = self.call_db(db_transactions.get, M.Ingest, self.ingest_id)
        if T.IngestStatus.is_terminal(ingest.status):  # type: ignore
            return ingest  # type: ignore
        if self.call_db(db_transactions.has_unfinished_tasks, self.ingest_id):
            return ingest  # type: ignore
        return self.call_db(db_transactions.start_singleton, self.ingest_id, T.TaskType.resolve)

    def start_detecting_duplicates(self) -> T.IngestOut:
        """Start detecting duplicates"""
        return self.call_db(db_transactions.start_singleton, self.ingest_id, T.TaskType.detect_duplicates)

    def resolve_subject(self, map_values: typing.List[str]) -> str:
        """Get existing or create new subject code based on the map values"""
        return self.call_db(db_transactions.resolve_subject, self.ingest_id, map_values)

    def start_finalizing(self) -> T.IngestOutAPI:
        """Set ingest status to finalizing and add finalize task if all uploads finished"""
        ingest = self.ingest
        if T.IngestStatus.is_terminal(ingest.status):
            return ingest
        if self.call_db(db_transactions.has_unfinished_tasks, self.ingest_id):
            return ingest
        return self.call_db(db_transactions.start_singleton, self.ingest_id, T.TaskType.finalize)

    def set_ingest_status(self, status: T.IngestStatus) -> T.IngestOut:
        """Set ingest status"""
        return self.call_db(db_transactions.set_ingest_status, self.ingest_id, status)

    def fail(self) -> T.IngestOut:
        """Set ingest status to failed and cancel pending tasks"""
        return self.call_db(db_transactions.fail_ingest, self.ingest_id)

    def batch_writer(self, *args, **kwargs) -> "BatchWriter":
        """Get batch writer which is bound to this client"""
        return BatchWriter(self, *args, **kwargs)

    def _iter_query(
        self,
        query: sqla.orm.Query,
        order_by_cols: typing.List[sqla.Column],
        schema: typing.Type[T.Schema],
        size: int = 10000
    ) -> typing.Iterable[typing.Any]:
        """Get all rows of the given query using seek method"""
        id_col = _get_id_column_from_query(query)
        columns = []
        for col in order_by_cols:
            if isinstance(col, sqla.sql.elements.Label):
                columns.append(col.element)
            else:
                columns.append(col)
        query = seek_query = query.order_by(*order_by_cols, id_col)
        while True:
            count = 0
            item = None
            for item in self.call_db(db_transactions.get_all, seek_query.limit(size), schema):
                count += 1
                yield item

            if count < size:
                break

            if item:
                values = []
                for col in order_by_cols:
                    values.append(getattr(item, col.name))
                seek_query = query.filter(sqla.sql.tuple_(*order_by_cols, id_col) > (*values, item.id))  # type: ignore
            else:
                break


class BatchWriter:
    """Batch insert/update writer of a given model"""

    def __init__(
        self,
        db: DBClient,
        type_: str,
        model_name: str,
        depends_on: "BatchWriter" = None,
        batch_size: int = 1000
    ):
        self.db = db  # pylint: disable=C0103
        self.type = type_
        self.model_name = model_name
        self.depends_on = depends_on
        self.batch_size = batch_size
        self.changes: typing.List[typing.Any] = []

    def push(self, change: typing.Any) -> None:
        """Push new change"""
        self.changes.append(change)
        if len(self.changes) >= self.batch_size:
            self.flush()

    def flush(self) -> None:
        """Flush all changes"""
        if self.depends_on:
            self.depends_on.flush()
        self.db.bulk(self.type, self.model_name, self.changes)
        self.changes = []


def _get_id_column_from_query(query: sqla.orm.Query) -> sqla.Column:
    """Get id column from the given query's column descriptions.

    Used to always order rows by a unique column in _iter_query.
    """
    for col_desc in query.column_descriptions:
        if inspect.isclass(col_desc["expr"]):
            return col_desc["expr"].id
        if col_desc["name"] == "id":
            return col_desc["expr"]
    raise ValueError("No id column detected in query")


def _get_paginate_order_by_col(model_cls: M.Base) -> sqla.Column:
    """Determine the primary order by column for a given model.

    If the model has a compound index for the paginator then return the index's second column,
    otherwise the ID column.
    """
    for index in model_cls.__table__.indexes:
        if isinstance(index, sqla.Index) and index.name.endswith("_paginate"):
            col = index.columns.items()[1][1]
            return getattr(model_cls, col.name)
    return model_cls.id


def _csv_field_str(field):
    """Stringify csv fields"""
    value = "" if field is None else str(field)
    if "," in value:
        value = f'"{value}"'
    return value


__all__ = [
    "DBClient"
]
