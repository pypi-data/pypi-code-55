import asyncpg
import collections

from typing import Type, Optional, OrderedDict, List, Set

from .models import Model, Meta
from .fields import ForeignKeyField, Action

from . import sql


class Database:
    """
    Database
    ========

    Database instance to interact with asyncpg.

    """

    #: Keep track of all the models defined in this database.
    models: OrderedDict[str, Type[Model]]

    debug : bool = False

    _pool : Optional[asyncpg.pool.Pool] = None

    def __init__(
            self,
            dsn : str,
            models : Optional[List[Model]] = None,
            debug=False,
            pool_kwargs=None
    ):
        # Initialize a Database instance.

        self.models = collections.OrderedDict()

        # Copy the list of models.
        models = [] if models is None else list(models)

        # Store the information for the pool
        self._dsn = dsn
        self._pool_kwargs = pool_kwargs if pool_kwargs is not None else {}

        # Sort the models in the right order.
        while len(models) > 0:

            model = models[0]

            deps = model._meta.depends

            if all(_ in self.models for _ in deps):
                self.models[model._meta.table_name] = models.pop(0)
            else:
                models.append(models.pop(0))

        # Resolve foreign keys.
        for table_name, model in self.models.items():
            for fname, field in model._meta.fields.items():
                if isinstance(field, ForeignKeyField):
                    self._resolve_foreign_field(field)

    def _resolve_foreign_field(self, field):

        reftable, refcolumn = field.refs()

        if refcolumn is None:

            # We accept only one primary key in this case.
            if len(self.models[reftable]._meta.primary_key) != 1:
                raise Exception(
                    "Composed primary keys are not supported."
                )

            # Resolve the field.
            refcolumn = self.models[reftable]._meta.primary_key[0]

        to_field = self.models[reftable]._meta.fields[refcolumn]
        field.resolve(refcolumn, to_field)

    def __await__(self):

        # Create the pool.
        self._pool = yield from asyncpg.create_pool(
            dsn=self._dsn, **self._pool_kwargs
        ).__await__()

        return self

    def acquire(self):
        return Connection(db=self)

    async def release(self, sess):
        await self._pool.release(sess.conn)

    # async def save(self, model, conn=None):

    #     if conn is None:
    #         conn = self._conn.get()

    #     # Update with values.
    #     values = {}

    #     # Find a where clause.
    #     where_clause = sql.WhereClause()

    #     # Find our pk.
    #     for name, field in model._meta.fields.items():
    #         if name in model._data and name in model._meta.primary_key:
    #             where_clause &= {name: model._data[name]}
    #         elif name in model._data:
    #             values[name] = model._data[name]
    #         elif name in model._data_default:
    #             values[name] = model._data_default[name]

    #     if where_clause:
    #         # Create an update.
    #         stmt = sql.PartialUpdate(
    #             conn, model._meta.table_name
    #         ).where(
    #             where_clause
    #         )
    #     else:
    #         # Insert statement
    #         stmt = sql.PartialInsert(
    #             conn, model._meta.table_name
    #         )

    #     # Update the rest.
    #     stmt.values(**values)

    #     stmt.returning(*model._meta.fields.keys())

    #     return model._update_data(**await stmt)


class Connection:
    def __init__(self, db):
        self.db = db

    def __await__(self):

        # Start a connection.
        self._conn = yield from self.db._pool.acquire().__await__()

        # Create a transaction.
        self._tr = self._conn.transaction()

        # Start the transaction.
        yield from self._tr.start().__await__()

        return self

    async def __aenter__(self):
        return await self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            await self._tr.commit()
        else:
            await self._tr.rollback()

        # Release the connection.
        await self.db._pool.release(self._conn)

    async def commit(self):
        await self._tr.commit()
        self._tr = self._conn.transaction()
        await self._tr.start()

    async def rollback(self):
        await self._tr.commit()
        self._tr = self._conn.transaction()
        await self._tr.start()

    async def _insert(self, instance):
        # Insert an instance into the database.

        stmt = sql.PartialInsert(
            table_name=instance._meta.table_name
        )

        # Set the values to insert using only our own fields.
        for fname in instance._meta.columns:

            if fname in instance._data:
                stmt.set_value(fname, instance._data[fname])

            elif fname in instance._data_default:
                stmt.set_value(fname, instance._data_default[fname])

        # Return all the columns.
        stmt.returning(*instance._meta.fields.keys())
        stmt.with_conn(self._conn)

        # Update the instance.
        record = await stmt

        return instance._update_data(**record)

    async def insert(self, instance):
        # Insert an instance into the database.

        if instance._meta.polymorphic_on is not None:

            instance._data[instance._meta.polymorphic_on] = \
                instance._meta.polymorphic_identity

            def _walk(meta : Meta) -> List[Model]:
                models = []

                for parent in meta.parents:

                    if parent not in models:
                        models.append(parent)

                    for _ in _walk(parent._meta):
                        if _ not in models:
                            models.append(_)

                return models

            models = _walk(instance._meta)
            if instance.__class__ not in models:
                models.insert(0, instance.__class__)

            models = list(reversed(models))

            instances = []

            for model in models:
                instance.__class__ = model
                instances.append(await self._insert(instance))

            return instances[-1]
        else:
            return await self._insert(instance)

    def delete(self, instance):

        # Create the delete statement.
        stmt = sql.PartialDelete(
            table_name=instance._meta.table_name,
            mapper=lambda x: instance.__class__(**x)
        )

        # Find the where clause.
        for name in instance._meta.primary_key:
            if name in instance._data:
                stmt.where(**{name: instance._data[name]})

        if not stmt._where:
            raise Exception("Instance has no primary key.")

        stmt.returning(*instance._meta.fields.keys())

        return stmt.with_conn(self._conn)

    def select(self, model):

        stmt = sql.PartialSelect(
            table_name=model._meta.table_name,
            mapper=lambda _: model(**_)
        )

        stmt.select(*list(model._meta.fields.keys()))
        stmt.with_conn(self._conn)

        return stmt

    async def update(self, instance):

        # Create an update.
        stmt = sql.PartialUpdate(
            table_name=instance._meta.table_name
        )

        # Find a where clause.
        where_clause = sql.WhereClause()

        # Define the where clause and the values to update.
        for name, field in instance._meta.fields.items():
            if name in instance._data and name in instance._meta.primary_key:
                where_clause &= {name: instance._data[name]}
            elif name in instance._data:
                stmt.set_value(name, instance._data[name])
            elif name in instance._data_default:
                stmt.set_value(name, instance._data_default[name])

        if not where_clause:
            raise Exception("Unable to determine a where clause.")

        # Add the where clause and the returning columns.
        stmt.where(where_clause)
        stmt.returning(*instance._meta.fields.keys())

        # Update data.
        record = await stmt.execute(conn=self._conn)

        return instance._update_data(**record)

    async def create_all_tables(self):

        # Sort the models in the right order.
        models_unsorted = list(self.db.models.keys())
        models_sorted = []

        while len(models_unsorted) > 0:

            key = models_unsorted[0]

            deps = self.db.models[key]._meta.depends

            if all(_ in models_sorted for _ in deps):
                models_sorted.append(models_unsorted.pop(0))
            else:
                models_unsorted.append(models_unsorted.pop(0))

        # Run all the statements inside a transaction.
        for table_name in models_sorted:
            await self.create_table(table_name)

    async def create_table(self, table_name : str):

        # Get the model.
        model = self.db.models[table_name]

        # Create table statement.
        stmt = sql.PartialCreateTable(
            table_name=table_name
        )

        for fname in model._meta.columns:

            # Get the definition of the field.
            field = model._meta.fields[fname]

            # Resolve the constraint.
            constraint = sql.ColumnConstraint(
                not_null=field.not_null,
                unique=field.unique,
            )

            if len(model._meta.primary_key) < 2:
                constraint.primary_key = field.primary_key

            # Resolve any dependecies.
            if isinstance(field, ForeignKeyField):
                reftable, refcolumn = field.refs()

                # Get the on_delete action.
                on_delete = None
                if isinstance(field.on_delete, Action):
                    on_delete = field.on_delete.value

                references = sql.ColumnConstraintReference(
                    reftable, refcolumn=refcolumn,
                    on_delete=on_delete
                )

                constraint.references = references

            # Append a new column.
            stmt.columns(**{
                fname: sql.ColumnClause(
                    field.__postgresql_type__(),
                    constraint
                )
            })

        # Append the table constraints
        if len(model._meta.primary_key) > 1:
            stmt.constraints(sql.TableConstraintPrimaryKey(
                keys=model._meta.primary_key
            ))

        # Attach a connection.
        stmt.with_conn(self._conn)

        await stmt
