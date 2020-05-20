# pylint: disable=E0213,W0613,R0201,R0903
"""SQLAlchemy DB models"""
import datetime
import json
import random
import string
import uuid

import sqlalchemy as sqla
from sqlalchemy import UnicodeText
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import UUIDType

from . import schemas as T


class JSONType(TypeDecorator): # pylint: disable=W0223
    """
    Use the base JSON type for any engine except Postgres where it uses JSONB
    """
    impl = UnicodeText

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(JSONB())

        return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            value = str(json.dumps(value))
        return value

    def process_result_value(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            value = json.loads(value)
        return value


Base = sqla.ext.declarative.declarative_base()  # pylint: disable=C0103


def create_tables(engine: sqla.engine.Engine) -> None:
    """Create all DB tables as defined by the models"""
    Base.metadata.create_all(engine)


class BaseMixin:
    """Mixin defining uuid primary key and schema serialization"""

    @sqla.ext.declarative.declared_attr
    def id(cls):  # pylint: disable=no-self-argument, invalid-name
        """ID primary key column (default: python-generated random uuid)"""
        return sqla.Column(UUIDType, primary_key=True, default=uuid.uuid4)

    @sqla.ext.declarative.declared_attr
    def created(cls):  # pylint: disable=no-self-argument, invalid-name
        """Created timestamp column (default: python-generated current dt)"""
        return sqla.Column(sqla.DateTime, index=True, default=datetime.datetime.utcnow)

    @classmethod
    def schema_cls(cls):
        """Get output schema class"""
        return getattr(T, f"{cls.__name__}Out", None) or getattr(T, f"{cls.__name__}")

    def schema(self):
        """Return sqla model as pydantic schema"""
        return self.schema_cls().from_orm(self)

class IngestRefMixin:
    """Mixin defining many-to-one relationship to an ingest"""
    @sqla.ext.declarative.declared_attr
    def ingest_id(cls):
        """Ingest ID foreign key column"""
        return sqla.Column(UUIDType, sqla.ForeignKey("ingest.id"), index=True)

    @sqla.ext.declarative.declared_attr
    def ingest(cls):
        """Ingest relationship with (pluralized) backref"""
        return sqla.orm.relationship("Ingest", backref=f"{cls.__tablename__}s")


class StatusMixin:
    """Mixin adding status, status change validation and history"""
    @property
    def status_enum(self):
        """Abstract property to be defined w/ the status enum class"""
        # NOTE not using abc to avoid interfering with model metaclass
        raise NotImplementedError

    @sqla.orm.validates("status")
    def validate_status(self, key, value):
        """Validate status change and add history record"""
        self.status_enum.validate_transition(self.status, value)
        if self.history is None:
            self.history = []
        new_status = self.status_enum.get_item(value).value
        self.history.append(create_history_record(new_status))
        sqla.orm.attributes.flag_modified(self, "history")
        return new_status


def generate_ingest_label():
    """Generate random ingest operation label"""
    rand = random.SystemRandom()
    chars = string.ascii_uppercase + string.digits
    return "".join(rand.choice(chars) for _ in range(8))


def create_history_record(status):
    """Create status history record (status, timestamp)"""
    return status, datetime.datetime.now(tz=datetime.timezone.utc).timestamp()


class Ingest(BaseMixin, StatusMixin, Base):
    """Ingest operation model"""
    __tablename__ = "ingest"
    modified = sqla.Column(sqla.DateTime, onupdate=datetime.datetime.utcnow)
    label = sqla.Column(sqla.String, unique=True, default=generate_ingest_label)
    api_key = sqla.Column(sqla.String)
    fw_host = sqla.Column(sqla.String)
    fw_user = sqla.Column(sqla.String)
    config = sqla.Column(sqla.JSON)
    strategy_config = sqla.Column(sqla.JSON)
    status = sqla.Column(sqla.String, default=T.IngestStatus.created)
    history = sqla.Column(sqla.JSON, default=lambda: [])

    status_enum = T.IngestStatus


class Task(BaseMixin, IngestRefMixin, StatusMixin, Base):
    """Task model"""
    __tablename__ = "task"
    __table_args__ = (sqla.Index("ix_proc_stats", "ingest_id", "status"),)
    modified = sqla.Column(sqla.DateTime, onupdate=datetime.datetime.utcnow)
    item_id = sqla.Column(UUIDType, sqla.ForeignKey("item.id"), index=True)
    item = sqla.orm.relationship("Item", backref=sqla.orm.backref("task", uselist=False))
    type = sqla.Column(sqla.String)
    context = sqla.Column(sqla.JSON)
    worker = sqla.Column(sqla.String)
    retries = sqla.Column(sqla.Integer, default=0)
    status = sqla.Column(sqla.String, default=T.TaskStatus.pending, index=True)
    history = sqla.Column(sqla.JSON, default=lambda: [])
    completed = sqla.Column(sqla.Integer, default=0)
    total = sqla.Column(sqla.Integer, default=0)

    status_enum = T.TaskStatus

    @sqla.orm.validates("type")
    def validate_type(self, key, value):
        """Validate task type"""
        return T.TaskType.get_item(value)


class Container(BaseMixin, IngestRefMixin, Base):
    """Container model which represents nodes in the destination hierarchy"""
    __tablename__ = "container"
    __table_args__ = (
        sqla.Index("ix_scan_stats", "ingest_id", "level"),
        sqla.Index("ix_container_paginate", "ingest_id", "path", "id"),
    )
    parent_id = sqla.Column(UUIDType, sqla.ForeignKey("container.id"), index=True)
    parent = sqla.orm.relationship("Container", remote_side="Container.id", backref="children")
    level = sqla.Column(sqla.Integer)
    path = sqla.Column(sqla.String)
    src_context = sqla.Column(sqla.JSON)
    dst_context = sqla.Column(sqla.JSON)
    dst_path = sqla.Column(sqla.String)

    @sqla.orm.validates("level")
    def validate_level(self, key, value):
        """Validate container level"""
        return T.ContainerLevel.get_item(value)


class Item(BaseMixin, IngestRefMixin, Base):
    """Ingest item model"""
    __tablename__ = "item"
    __table_args__ = (
        sqla.Index("ix_item_paginate", "ingest_id", "dir", "id"),
    )
    container_id = sqla.Column(UUIDType, sqla.ForeignKey("container.id"), index=True)
    container = sqla.orm.relationship("Container", backref="items")
    dir = sqla.Column(sqla.String)
    type = sqla.Column(sqla.String)
    files = sqla.Column(sqla.JSON)
    filename = sqla.Column(sqla.String)
    files_cnt = sqla.Column(sqla.Integer)
    bytes_sum = sqla.Column(sqla.BigInteger)
    context = sqla.Column(sqla.JSON)
    existing = sqla.Column(sqla.Boolean)
    skipped = sqla.Column(sqla.Boolean)

    @sqla.orm.validates("type")
    def validate_type(self, key, value):
        """Validate item type"""
        return T.ItemType.get_item(value)


class Review(BaseMixin, IngestRefMixin, Base):
    """Review model"""
    __tablename__ = "review"
    path = sqla.Column(sqla.String)
    skip = sqla.Column(sqla.Boolean)
    context = sqla.Column(sqla.JSON)


class Subject(BaseMixin, IngestRefMixin, Base):
    """Subject model"""
    __tablename__ = "subject"
    __table_args__ = (
        sqla.Index("ix_subject_paginate", "ingest_id", "code", "id"),
        sqla.Index("ix_subject_resolve", "ingest_id", "map_values"),
    )
    code = sqla.Column(sqla.String)
    map_values = sqla.Column(JSONType)


class DeidLog(BaseMixin, IngestRefMixin, Base):
    """Deid log model"""
    __tablename__ = "deid_log"
    __table_args__ = (sqla.Index("ix_deidlog_paginate", "ingest_id", "created", "id"),)
    src_path = sqla.Column(sqla.String)
    tags_before = sqla.Column(sqla.JSON)
    tags_after = sqla.Column(sqla.JSON)


class Error(BaseMixin, IngestRefMixin, Base):
    """Holds item related error"""
    __tablename__ = "item_error"
    __table_args__ = (sqla.Index("ix_item_error_paginate", "ingest_id", "created", "id"),)
    item_id = sqla.Column(UUIDType, sqla.ForeignKey("item.id"), index=True)
    item = sqla.orm.relationship("Item", backref="errors")
    task_id = sqla.Column(UUIDType, sqla.ForeignKey("task.id"), index=True)
    task = sqla.orm.relationship("Task", backref="errors")
    filepath = sqla.Column(sqla.String)
    code = sqla.Column(sqla.String)
    # allow to store unknown/dynamic error messages
    # mainly used in the asbtarct task error handle to capture any
    # unhandled exceptions
    message = sqla.Column(sqla.String)

sqla.orm.configure_mappers()  # NOTE create backrefs
