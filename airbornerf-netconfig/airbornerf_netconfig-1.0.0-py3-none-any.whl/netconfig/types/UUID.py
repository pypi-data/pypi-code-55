# Backend-agnostic UUID Type
# Receives and returns Python uuid() objects. Uses the PG UUID type when using PostgreSQL, CHAR(32) on other backends,
# storing them in stringified hex format. Can be modified to store binary in CHAR(16) if desired.
# Inspired from https://docs.sqlalchemy.org/en/13/core/custom_types.html#backend-agnostic-guid-type

from sqlalchemy.types import TypeDecorator, CHAR
import sqlalchemy.dialects.postgresql
import uuid


class UUID(TypeDecorator):
    """Platform-independent UUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(sqlalchemy.dialects.postgresql.UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value