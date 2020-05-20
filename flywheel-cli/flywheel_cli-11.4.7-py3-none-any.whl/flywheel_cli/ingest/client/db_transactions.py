# pylint: disable=W0143
"""Transactions for the DBClient"""

import typing
import uuid
import re

import sqlalchemy as sqla

from .. import models as M
from .. import schemas as T
from .. import errors

# Transactional crud methods

def add(db: sqla.orm.Session, model: M.Base) -> T.Schema:
    """Add an object"""
    db.add(model)
    db.flush()
    return model.schema()


def get(db: sqla.orm.Session, model_cls: typing.Type[M.Base], id_: uuid.UUID) -> T.Schema:
    """Get object by ID"""
    return db.query(model_cls).filter(model_cls.id == id_).one().schema()


def get_all(
    db: sqla.orm.Session,
    query: sqla.orm.Query,
    schema: T.Schema,
) -> typing.List[T.Schema]:
    """Get all object that match the given query"""
    return [schema.from_orm(model) for model in query.with_session(db).all()]


def count_all(db: sqla.orm.Session, ingest_id: uuid.UUID, model_cls: typing.Type[M.Base]) -> int:
    """Get count of row for the specified model"""
    return (
        db.query(sqla.sql.func.count(model_cls.id).label("count"))
        .filter(model_cls.ingest_id == ingest_id)
        .scalar()
    )


def update(
    db: sqla.orm.Session,
    model_cls: M.Base,
    id_: uuid.UUID,
    **updates: typing.Any
) -> T.Schema:
    """Update an object with the given update set"""
    query = db.query(model_cls).filter(model_cls.id == id_)
    query.update(updates)
    db.flush()
    return query.one().schema()


def find_one(
    db: sqla.orm.Session,
    model_cls: M.Base,
    *conditions: typing.Any,
) -> T.Schema:
    """Find one matching row for the given model."""
    query = db.query(model_cls)
    for condition in conditions:
        query = query.filter(condition)
    return query.one().schema()


def bulk(
    db: sqla.orm.Session, type_: str, model_cls: M.Base, mappings: typing.List[typing.Any]
) -> None:
    """Perform a bulk insert/update of the given list of mapping dictionaries"""
    assert type_ in ("insert", "update")
    bulk_method = getattr(db, f"bulk_{type_}_mappings")
    bulk_method(model_cls, mappings)
    db.flush()


def start(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.IngestOut:
    """Start the ingest, set ingest status to scanning and kick off
    the initial template scan task.

    Lock on the ingest row until the transaction ends to prevent starting
    multiple initial scan tasks.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    assert ingest.status == T.IngestStatus.created
    ingest.status = T.IngestStatus.scanning
    db.add(M.Task(
        ingest_id=ingest_id,
        type=T.TaskType.scan,
        context={"scanner": {"type": "template", "dir": "/"}},
    ))
    db.flush()
    return ingest.schema()


def review(
    db: sqla.orm.Session, ingest_id: uuid.UUID, changes: typing.Optional[T.ReviewIn] = None
) -> T.IngestOut:
    """Save review and start preparing, set ingest status to preparing and kick off
    the prepare task.

    Lock on the ingest row until the transaction ends to prevent starting multiple
    prepare tasks.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    assert ingest.status == T.IngestStatus.in_review
    ingest.status = T.IngestStatus.preparing
    if changes is not None:
        for change in changes:
            db.add(M.Review(ingest_id=ingest_id, **change.dict()))
    db.add(M.Task(ingest_id=ingest_id, type=T.TaskType.prepare))
    db.flush()
    return ingest.schema()


def abort(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.IngestOut:
    """Abort the ingest, set ingest status to aborted and cancel all pending
    tasks.

    Lock on the ingest row until the transaction ends to prevent setting ingest/tasks
    statuses multiple times.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    if ingest.status == T.IngestStatus.aborted:
        return ingest.schema()
    ingest.status = T.IngestStatus.aborted
    _cancel_pending_tasks(db, ingest_id)
    db.flush()
    return ingest.schema()


def next_task(db: sqla.orm.Session, worker: str) -> typing.Optional[T.TaskOut]:
    """Get next task which's status is pending and set the status to running.

    Lock on the first task that match and skip any locked ones. This prevents the
    workers to grab the same task.
    """
    query = _for_update(
        db.query(M.Task).filter(M.Task.status == T.TaskStatus.pending),
        skip_locked=True,
    )
    task = query.first()
    if task is None:
        return None
    task.worker = worker
    task.status = T.TaskStatus.running
    db.flush()
    return task.schema()


def get_progress(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.Progress:
    """Get ingest scan task and item/file/byte counts by status"""
    progress = T.Progress().dict()
    scan_tasks_by_status = (
        db.query(
            M.Task.status,
            sqla.sql.func.count(M.Task.id).label("count"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.type == T.TaskType.scan,
        )
        .group_by(M.Task.status)
    )
    for row in scan_tasks_by_status:
        progress["scans"][row.status] = row.count
        progress["scans"]["total"] += row.count
        if T.TaskStatus.is_terminal(row.status):
            progress["scans"]["finished"] += row.count

    tasks_by_type = (
        db.query(
            M.Task.type,
            sqla.sql.func.sum(M.Task.completed).label("completed"),
            sqla.sql.func.sum(M.Task.total).label("total"),
        )
        .filter(
            M.Task.ingest_id == ingest_id,
        )
        .group_by(M.Task.type)
    )
    for row in tasks_by_type:
        progress["stages"][T.TaskType.ingest_status(row.type)]["completed"] = row.completed
        progress["stages"][T.TaskType.ingest_status(row.type)]["total"] = row.total

    items_by_status = (
        db.query(
            M.Task.status,
            M.Item.skipped,
            sqla.sql.func.count(M.Item.id).label("items"),
            sqla.sql.func.sum(M.Item.files_cnt).label("files"),
            sqla.sql.func.sum(M.Item.bytes_sum).label("bytes"),
        )
        .outerjoin(M.Item.task)  # pylint: disable=E1101
        .filter(M.Item.ingest_id == ingest_id)
        .group_by(M.Task.status, M.Item.skipped)
    )
    for row in items_by_status.all():
        if row.skipped:
            # items skipped via review tracked separately
            status = "skipped"
        elif row.status is None:
            # items that don't have any (upload task) status yet
            status = "scanned"
        else:
            # items with an upload task tracked as the task status
            status = row.status

        for attr in ("items", "files", "bytes"):
            progress[attr][status] = getattr(row, attr)
            progress[attr]["total"] += getattr(row, attr)
            if T.TaskStatus.is_terminal(status):
                progress[attr]["finished"] += getattr(row, attr)
    return T.Progress(**progress)


def get_summary(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.Summary:
    """Get ingest hierarchy node and file count by level and type"""
    summary = {}
    containers_by_level = (
        db.query(
            M.Container.level,
            sqla.sql.func.count(M.Container.id).label("count"))
        .filter(M.Container.ingest_id == ingest_id)
        .group_by(M.Container.level)
    )
    for row in containers_by_level.all():
        level_name = T.ContainerLevel.get_item(row.level).name
        summary[f"{level_name}s"] = row.count
    items_by_type = (
        db.query(
            M.Item.type,
            sqla.sql.func.count(M.Item.id).label("count"))
        .filter(M.Item.ingest_id == ingest_id)
        .group_by(M.Item.type)
    )
    for row in items_by_type.all():
        summary[f"{row.type}s"] = row.count
    errors_by_type = (
        db.query(
            M.Error.code,
            sqla.sql.func.count(M.Error.id).label("count")
        )
        .filter(M.Error.ingest_id == ingest_id)
        .group_by(M.Error.code)
    )
    for row in errors_by_type.all():
        error = errors.get_error_by_code(row.code)
        summary.setdefault("errors", []).append({
            "code": error.code,
            "message": error.message,
            "description": error.description,
            "count": row.count,
        })
    return T.Summary(**summary)


def get_report(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.Report:
    """Get ingest status, elapsed time per status and list of failed tasks"""
    ingest = _get_ingest(db, ingest_id)
    elapsed = {}
    for old, new in zip(ingest.history, ingest.history[1:]):
        old_status, old_timestamp = old
        new_status, new_timestamp = new  # pylint: disable=W0612
        elapsed[old_status] = new_timestamp - old_timestamp
    task_errors_query = (
        db.query(
            M.Task.id.label("task"),  # pylint: disable=E1101
            M.Task.type,
            M.Error.code,
            M.Error.message,
            M.Error.filepath,
        )
        .join(M.Task.errors)  # pylint: disable=E1101
        .filter(
            M.Task.ingest_id == ingest_id,
        )
        .order_by(M.Task.created)
    )
    task_errors = []
    for error in task_errors_query.all():
        message = error.message or errors.get_error_by_code(error.code).message
        if error.filepath:
            message = f"{error.filepath}: {message}"
        task_errors.append(T.TaskError(
            task=error.task,
            type=error.type,
            code=error.code,
            message=message,
        ))
    return T.Report(
        status=ingest.status,
        elapsed=elapsed,
        errors=task_errors,
    )


def start_singleton(db: sqla.orm.Session, ingest_id: uuid.UUID, type_: T.TaskType) -> T.IngestOut:
    """Start singleton task (resolve, finalize).

    Lock on the ingest row until the transaction ends to prevent strating singletons multiple times.
    """
    # all scan tasks finished - lock the ingest
    ingest = _get_ingest(db, ingest_id, for_update=True)
    # set status and add scan task (once - noop for 2nd worker)
    if ingest.status != T.TaskType.ingest_status(type_) and not T.IngestStatus.is_terminal(ingest.status):
        ingest.status = T.TaskType.ingest_status(type_)
        db.add(M.Task(ingest_id=ingest_id, type=type_))
        db.flush()
    return ingest.schema()


def has_unfinished_tasks(db: sqla.orm.Session, ingest_id: uuid.UUID) -> bool:
    """Return true if there are penging/running tasks otherwise false"""
    pending_or_running = (
        db.query(M.Task.id)
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.status.in_([T.TaskStatus.pending, T.TaskStatus.running])
        )
    )
    return bool(pending_or_running.count())


def has_running_tasks(db: sqla.orm.Session, ingest_id: uuid.UUID) -> bool:
    """Return true if there are penging/running tasks otherwise false"""
    running = (
        db.query(M.Task.id)
        .filter(
            M.Task.ingest_id == ingest_id,
            M.Task.status.in_([T.TaskStatus.running])
        )
    )
    return bool(running.count())


def resolve_subject(
    db: sqla.orm.Session, ingest_id: uuid.UUID, map_values: typing.List[str]
) -> str:
    """Get existing or create new subject code based on the map values"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    subject = (
        db.query(M.Subject)
        .filter(
            M.Subject.ingest_id == ingest_id,
            M.Subject.map_values == map_values,
        )
        .first()
    )
    if subject is None:
        subject_config = ingest.config["subject_config"]
        subject_config["code_serial"] += 1
        sqla.orm.attributes.flag_modified(ingest, "config")
        subject = M.Subject(
            ingest_id=ingest_id,
            code=subject_config["code_format"].format(
                SubjectCode=subject_config["code_serial"]
            ),
            map_values=map_values,
        )
        db.add(subject)
        db.flush()
    return subject.code


def set_ingest_status(
    db: sqla.orm.Session, ingest_id: uuid.UUID, status: T.IngestStatus
) -> T.IngestOut:
    """Set ingest status"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    if ingest.status != status:
        ingest.status = status
        db.flush()
    return ingest.schema()


def fail_ingest(db: sqla.orm.Session, ingest_id: uuid.UUID) -> T.IngestOut:
    """Set ingest status to failed and cancel pending tasks"""
    ingest = _get_ingest(db, ingest_id, for_update=True)
    ingest.status = T.IngestStatus.failed
    _cancel_pending_tasks(db, ingest_id)
    db.flush()
    return ingest.schema()


def load_subject_csv(
    db: sqla.orm.Session, ingest_id: uuid.UUID, subject_csv: typing.BinaryIO
) -> None:
    """Load subject codes from csv file.

    Lock on the ingest row to prevent mixing different subject configs.
    """
    ingest = _get_ingest(db, ingest_id, for_update=True)
    subject_config = ingest.config.setdefault("subject_config", {})
    header = subject_csv.readline().decode("utf8").strip()
    code_format, *map_keys = header.split(",")
    if subject_config:
        assert map_keys == subject_config["map_keys"]
    else:
        subject_config["code_format"] = code_format
        subject_config["map_keys"] = map_keys
    subject_config.setdefault("code_serial", 0)

    code_re = re.compile(r"^[^\d]*(\d+)[^\d]*$")
    for line in subject_csv:
        subject = line.decode("utf8").strip()
        code, *map_values = subject.split(",")
        match = code_re.match(code)
        if not match:
            raise ValueError(f"Invalid code in subject csv: {code}")
        code_int = int(match.group(1))
        if code_int > subject_config["code_serial"]:
            subject_config["code_serial"] = code_int
        # NOTE all subjects in memory
        db.add(M.Subject(
            ingest_id=ingest_id,
            code=code,
            map_values=map_values,
        ))
    sqla.orm.attributes.flag_modified(ingest, "config")
    db.flush()

def delete_ingest(db: sqla.orm.Session, ingest_id: uuid.UUID) -> None:
    """Delete an ingest and all related records"""

    # delete Subject, DeidLog, Review
    _delete(db, M.Subject, M.Subject.ingest_id == ingest_id)
    _delete(db, M.DeidLog, M.DeidLog.ingest_id == ingest_id)
    _delete(db, M.Review, M.Review.ingest_id == ingest_id)

    # execution order is important from now on because of the foreign keys
    _delete(db, M.Task, M.Task.ingest_id == ingest_id)
    _delete(db, M.Item, M.Item.ingest_id == ingest_id)

    # deletion in reverse ContainerLevel order (parent-child realtions)
    _delete(db, M.Container, sqla.and_(
            M.Container.ingest_id == ingest_id,
            M.Container.level == T.ContainerLevel.acquisition
    ))
    _delete(db, M.Container, sqla.and_(
            M.Container.ingest_id == ingest_id,
            M.Container.level == T.ContainerLevel.session
    ))
    _delete(db, M.Container, sqla.and_(
            M.Container.ingest_id == ingest_id,
            M.Container.level == T.ContainerLevel.subject
    ))
    _delete(db, M.Container, sqla.and_(
            M.Container.ingest_id == ingest_id,
            M.Container.level == T.ContainerLevel.project
    ))
    _delete(db, M.Container, sqla.and_(
            M.Container.ingest_id == ingest_id,
            M.Container.level == T.ContainerLevel.group
    ))

    _delete(db, M.Ingest, M.Ingest.id == ingest_id)

# Helpers

def _get_ingest(db: sqla.orm.Session, ingest_id: uuid.UUID, for_update: bool = False) -> M.Ingest:
    """Get ingest by ID and locks on it if requested"""
    query = db.query(M.Ingest).filter(M.Ingest.id == ingest_id)
    if for_update:
        query = _for_update(query)
    return query.one()


def _for_update(query: sqla.orm.Query, skip_locked: bool = False) -> sqla.orm.Query:
    """Lock as granularly as possible for given query and backend"""
    # with_for_update() locks selected rows in postgres
    # (ignored w/ sqlite, but its not a problem, since we use immediate transactions there)
    # skip_locked silently skips over records that are currently locked
    # populate_existing to get objects with the latest modifications
    # see: https://github.com/sqlalchemy/sqlalchemy/issues/4774
    return query.with_for_update(skip_locked=skip_locked).populate_existing()


def _cancel_pending_tasks(db: sqla.orm.Session, ingest_id: uuid.UUID) -> None:
    """Cancel all pending tasks"""
    pending_tasks = db.query(M.Task).filter(
        M.Task.ingest_id == ingest_id,
        M.Task.status == T.TaskStatus.pending,
    )
    pending_tasks.update({M.Task.status: T.TaskStatus.canceled})


def _delete(db: sqla.orm.Session, model, *conditions):
    """Delete from DB

    Used to delete non-fetched records
    """
    db.execute(model.__table__.delete().where(*conditions))
