import logging
import dataclasses
import asyncpg

from .exceptions import EmptySelection, MultipleRowsSelected


from typing import Dict, Optional, List, Any, Union


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclasses.dataclass
class StatementContext:
    values : List[Any] = dataclasses.field(default_factory=list)


class Statement:
    def __stmt__(self, ctx : StatementContext):
        # Statements are built using the magic method __stmt__
        return str(self)


@dataclasses.dataclass
class ColumnConstraintReference:
    reftable: str
    refcolumn: Optional[str] = None
    on_delete: Optional[str] = None
    on_update: Optional[str] = None

    def __str__(self):
        stmt = f'REFERENCES "{self.reftable}"'

        if self.refcolumn:
            stmt = f'{stmt} ("{self.refcolumn}")'

        if self.on_delete:
            stmt = f'{stmt} ON DELETE {self.on_delete}'

        return stmt


@dataclasses.dataclass
class TableConstraint(Statement):
    pass


@dataclasses.dataclass
class TableConstraintPrimaryKey(TableConstraint):
    keys : List[str] = dataclasses.field(default_factory=list)

    def __bool__(self):
        return len(self.keys) > 0

    def __stmt__(self, ctx):
        keys = ', '.join(f'"{k}"' for k in self.keys)
        return f'PRIMARY KEY ({keys})'


@dataclasses.dataclass
class ColumnConstraint:
    not_null: bool = False
    primary_key: bool = False
    references: Optional[ColumnConstraintReference] = None
    unique : bool = False

    def __bool__(self):

        if self.not_null:
            return True

        if self.primary_key:
            return True

        if self.references:
            return True

        if self.unique:
            return True

        return False

    def __str__(self):

        constraints = []

        if self.not_null:
            constraints.append("NOT NULL")

        if self.unique:
            constraints.append("UNIQUE")

        if self.primary_key:
            constraints.append("PRIMARY KEY")

        if self.references:
            constraints.append(str(self.references))

        return " ".join(constraints)


@dataclasses.dataclass
class ColumnClause(Statement):
    data_type : str
    constraint : Optional[ColumnConstraint] = None

    def __stmt__(self, ctx):
        stmt = f'{self.data_type}'

        if self.constraint:
            stmt = f"{stmt} {self.constraint}"
        return stmt


@dataclasses.dataclass
class WhereClause(Statement):
    def __bool__(self):
        return False

    def __and__(self, other):

        if isinstance(other, dict):
            parts = []
            for n, v in other.items():
                lhs = ExpressionColumnName(n)
                rhs = ExpressionLiteralValue(v)
                parts.append(WhereClauseEquality(lhs=lhs, rhs=rhs))
            return WhereClauseAnd(parts=parts)

        if isinstance(other, WhereClauseAnd):
            return WhereClauseAnd(parts=other.parts)

        if isinstance(other, WhereClause):
            return WhereClauseAnd(parts=[other])

        raise NotImplementedError("Operation not implemented")


@dataclasses.dataclass
class SetClause(Statement):
    values : Dict[str, Any] = dataclasses.field(default_factory=dict)

    def __bool__(self):
        return len(self.values) > 0

    def __stmt__(self, ctx):
        set_values = []
        for name, value in self.values.items():
            ctx.values.append(value)
            set_values.append(f'"{name}"=${len(ctx.values)}')

        return ', '.join(set_values)


@dataclasses.dataclass
class ReturningClause(Statement):
    names : List[str] = dataclasses.field(default_factory=list)

    def __bool__(self):
        return len(self.names) > 0

    def __stmt__(self, ctx):
        return ', '.join(f'"{name}"' for name in self.names)

    def __call__(self, *args):
        self.names.extend(args)


@dataclasses.dataclass
class SelectClause(Statement):
    names : List[str] = dataclasses.field(default_factory=list)

    def __bool__(self):
        return len(self.names) > 0

    def __stmt__(self, ctx):
        return ', '.join(f'"{name}"' for name in self.names)


@dataclasses.dataclass
class ValuesClause(Statement):
    values : Dict[str, Any] = dataclasses.field(default_factory=dict)

    def __bool__(self):
        return len(self.values) > 0

    def __stmt__(self, ctx):

        cols = []
        placeholders = []

        for name, value in self.values.items():
            ctx.values.append(value)
            cols.append(f'"{name}"')
            placeholders.append(f'${len(ctx.values)}')

        return f'({", ".join(cols)}) VALUES ({", ".join(placeholders)})'


class Expression(Statement):
    def __bool__(self):
        return False


@dataclasses.dataclass
class WhereClauseEquality(WhereClause):
    lhs: Union[Expression, str]
    rhs: Union[Expression, str]

    def __bool__(self):
        return True

    def __stmt__(self, ctx):
        return f'{self.lhs.__stmt__(ctx)}={self.rhs.__stmt__(ctx)}'


@dataclasses.dataclass
class WhereClauseAnd(WhereClause):
    parts: List[WhereClause] = dataclasses.field(default_factory=list)

    def __bool__(self):
        return len(self.parts) > 0

    def __str__(self):
        return " AND ".join(f'({_})' for _ in self.parts)

    def __stmt__(self, ctx):
        return " AND ".join(f'{_.__stmt__(ctx)}' for _ in self.parts)

    def __and__(self, other):
        # `and` operation between WhereClause's.

        if isinstance(other, WhereClauseAnd):
            return WhereClauseAnd(parts=self.parts + other.parts)

        if isinstance(other, WhereClause):
            return WhereClauseAnd(parts=self.parts + [other])

        if isinstance(other, dict):
            return self & (WhereClause() & other)

        raise NotImplementedError("Operation not implemented")


@dataclasses.dataclass
class ExpressionColumnName(Expression):
    name : str

    def __bool__(self):
        return self.name != ""

    def __str__(self):
        return f'"{self.name}"'


@dataclasses.dataclass
class ExpressionLiteralValue(Expression):
    value : Any

    def __bool__(self):
        return str(self.value) != ""

    def __stmt__(self, ctx):

        ctx.values.append(self.value)

        i = len(ctx.values)

        return f'${i}'


class Asterisk(Expression):
    def __bool__(self):
        return True

    def __str__(self):
        return '*'


@dataclasses.dataclass
class WhereMixin:

    _where : WhereClause = dataclasses.field(
        init=False, default_factory=WhereClause
    )

    def where(self, *args, **kwargs):

        # When args are passed are considered to be where clauses.
        for arg in args:
            self._where &= arg

        for name, value in kwargs.items():
            lhs = ExpressionColumnName(name=name)
            rhs = ExpressionLiteralValue(value=value)
            self._where &= WhereClauseEquality(lhs=lhs, rhs=rhs)

        return self


@dataclasses.dataclass
class ReturningMixin:

    _returning : ReturningClause = dataclasses.field(
        init=False, default_factory=ReturningClause
    )

    def returning(self, *names):
        self._returning.names.extend(names)


@dataclasses.dataclass
class SelectMixin:

    _select : SelectClause = dataclasses.field(
        init=False, default_factory=SelectClause
    )

    def select(self, *names):
        self._select.names.extend(names)
        return self


@dataclasses.dataclass
class ValuesMixin:
    _values : ValuesClause = dataclasses.field(
        init=False, default_factory=ValuesClause
    )

    def values(self, **kwargs):
        self._values.values.update(kwargs)
        return self

    def set_value(self, key, value):
        self._values.values[key] = value


@dataclasses.dataclass
class SetMixin:
    _set : SetClause = dataclasses.field(
        init=False, default_factory=SetClause
    )

    def values(self, **kwargs):
        self._set.values.update(kwargs)
        return self

    def set_value(self, key, value):
        self._set.values[key] = value


@dataclasses.dataclass
class Command:
    conn : asyncpg.Connection = dataclasses.field(
        init=False
    )

    async def execute(self, conn=None):
        if conn is not None:
            self.conn = conn
        return await self

    def with_conn(self, conn):
        self.conn = conn
        return self


@dataclasses.dataclass
class PartialDelete(Command, WhereMixin, ReturningMixin):

    table_name : str

    mapper : Optional[callable] = None

    def __await__(self):

        # Start with a statement context.
        ctx = StatementContext()

        stmt = f'DELETE FROM "{self.table_name}"'

        # Append a where clause (Mmm, en error here could
        # delete a whole table.)
        if self._where:
            stmt = f'{stmt} WHERE {self._where.__stmt__(ctx)}'

        # Append the returning columns.
        if self._returning:
            stmt = f"{stmt} RETURNING ({self._returning.__stmt__(ctx)})"

        logger.debug(stmt)
        record = yield from self.conn.fetch(stmt, *ctx.values).__await__()

        if self._returning:
            return {k: v for k, v in zip(self._returning.names, record['row'])}

        return None


@dataclasses.dataclass
class PartialUpdate(Command, WhereMixin, ReturningMixin, SetMixin):

    table_name : str

    mapper : Optional[callable] = None

    def __await__(self):

        # Start with a statement context.
        ctx = StatementContext()

        stmt = f'UPDATE "{self.table_name}"'

        # Append a set clause.
        if self._set:
            stmt = f'{stmt} SET {self._set.__stmt__(ctx)}'

        # Append a where clause.
        if self._where:
            stmt = f'{stmt} WHERE {self._where.__stmt__(ctx)}'

        # Append the returning columns.
        if self._returning:
            stmt = f"{stmt} RETURNING ({self._returning.__stmt__(ctx)})"

        # Wait for the update.
        logger.debug(stmt)
        record = yield from self.conn.fetchrow(stmt, *ctx.values).__await__()

        if self._returning:
            record = {k: v for k, v in zip(self._returning.names, record['row'])}
            if callable(self.mapper):
                return self.mapper(record)
            return record

        return None


@dataclasses.dataclass
class PartialSelect(Command, WhereMixin, SelectMixin):

    table_name : str

    mapper : Optional[callable] = None

    _one : bool = dataclasses.field(init=False, default=False)

    def one(self, conn=None):
        #: Return one instance of a model or raise an error.
        self._one = True
        return self

    def __await__(self):

        # Count first.
        ctx = StatementContext()
        stmt = f'SELECT COUNT(*) FROM "{self.table_name}"'

        if self._where:
            stmt = f"{stmt} WHERE {self._where.__stmt__(ctx)}"

        logger.debug(stmt)
        count = yield from self.conn.fetchval(stmt, *ctx.values).__await__()

        if count == 0:
            raise EmptySelection

        if self._one and count >= 2:
            raise MultipleRowsSelected

        # Select the single row now.
        ctx = StatementContext()
        stmt = f'SELECT {self._select.__stmt__(ctx)} FROM "{self.table_name}"'

        if self._where:
            stmt = f"{stmt} WHERE {self._where.__stmt__(ctx)}"

        if self._one:

            stmt = f"{stmt} LIMIT 1"

            # Wait for the update.
            logger.debug(stmt)
            records = yield from self.conn.fetch(stmt, *ctx.values).__await__()

            if callable(self.mapper):
                return self.mapper(records[0])

            return records[0]

        else:

            # Wait for the update.
            logger.debug(stmt)
            records = yield from self.conn.fetch(stmt, *ctx.values).__await__()

            if callable(self.mapper):
                return [self.mapper(_) for _ in records]

            return records


@dataclasses.dataclass
class PartialInsert(Command, ReturningMixin, ValuesMixin):
    """
    INSERT Command
    ==============

    Construct an INSERT command and execute it when awaited.
    """

    table_name : str

    mapper : Optional[callable] = None

    def __await__(self):

        ctx = StatementContext()

        stmt = f'INSERT INTO "{self.table_name}"'

        if self._values:
            stmt = f"{stmt} {self._values.__stmt__(ctx)}"

        if self._returning:
            stmt = f"{stmt} RETURNING ({self._returning.__stmt__(ctx)})"

        logger.debug(stmt)
        record = yield from self.conn.fetchrow(stmt, *ctx.values).__await__()

        if self._returning:
            record = {k: v for k, v in zip(self._returning.names, record['row'])}
            if callable(self.mapper):
                return self.mapper(record)
            return record

        return None


@dataclasses.dataclass
class PartialCreateTable(Command):

    table_name : str

    _columns : Dict[str, ColumnClause] = dataclasses.field(
        default_factory=dict
    )

    _constraints : List[TableConstraint] = dataclasses.field(
        default_factory=list
    )

    def columns(self, **kwargs):
        self._columns.update(kwargs)
        return self

    def constraints(self, *args):
        self._constraints.extend(args)
        return self

    def __await__(self):

        ctx = StatementContext()

        stmt = f'CREATE TABLE IF NOT EXISTS "{self.table_name}"'

        # Columns and constraints are mixed.
        columns_and_constraints = []

        for name, col in self._columns.items():
            columns_and_constraints.append(f'"{name}" {col.__stmt__(ctx)}')

        for cons in self._constraints:
            if cons:
                columns_and_constraints.append(f'{cons.__stmt__(ctx)}')

        if columns_and_constraints:
            stmt = f'{stmt} ({", ".join(columns_and_constraints)})'

        logger.debug(stmt)
        yield from self.conn.execute(stmt).__await__()
