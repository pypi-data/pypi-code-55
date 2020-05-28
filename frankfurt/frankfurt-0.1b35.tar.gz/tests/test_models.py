from uuid import uuid4
import pytest
from mock import call


def test_simple_model():

    from frankfurt.models import Model
    from frankfurt import fields

    class Example(Model):
        text = fields.CharField(max_length=200)

    example = Example(text='test')
    assert example['text'] == 'test'

    with pytest.raises(KeyError):
        example['text_3']


def test_exception_incorrect_argument():
    from frankfurt.models import Model
    from frankfurt import fields

    class Example(Model):
        text = fields.CharField(max_length=200)

    with pytest.raises(TypeError):
        Example(another='test')


def test_abstract_model():

    from frankfurt.models import Model

    class Example(Model):
        class Meta:
            abstract = True

    assert Example._meta.abstract


@pytest.mark.asyncio
async def test_two_primary_keys(asyncpg_conn):
    from frankfurt import Database
    from frankfurt import fields
    from frankfurt.models import Model

    class Book(Model):
        author = fields.CharField(max_length=200, primary_key=True)
        title = fields.CharField(max_length=200, primary_key=True)

    # Get a session.
    db = await Database('__url__', models=[Book])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    # Assert the creation.
    asyncpg_conn.execute.assert_awaited_once_with(
        'CREATE TABLE IF NOT EXISTS "book" ('
        '"author" VARCHAR(200), "title" VARCHAR(200), '
        'PRIMARY KEY ("author", "title"))'
    )


def test_inherit_fields():
    from frankfurt import fields
    from frankfurt.models import Model

    class Writer(Model):
        pk = fields.UUIDField(primary_key=True)
        full_name = fields.CharField(max_length=400)

        class Meta:
            table_name = 'writers'

    class BaseModel(Model):
        pk = fields.UUIDField(primary_key=True)
        creation_date = fields.DateTimeField(auto_now_add=True)
        writer = fields.ForeignKeyField(to='writers')

        class Meta:
            abstract = True

    class Book(BaseModel):
        title = fields.CharField(max_length=200)

    # Check that book has the right fields.
    assert 'pk' in Book._meta.fields
    assert 'creation_date' in Book._meta.fields
    assert 'writer' in Book._meta.fields

    # Check that the fields are new instances.
    assert BaseModel._meta.fields['pk'] == Book._meta.fields['pk']


@pytest.mark.asyncio
async def test_create_table_from_model(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Writer(Model):
        pk = fields.UUIDField(primary_key=True)
        full_name = fields.CharField(max_length=400)

        class Meta:
            table_name = 'writers'

    class Book(Model):
        title = fields.CharField(max_length=200)
        date = fields.DateTimeField()
        author = fields.ForeignKeyField(
            to='writers', on_delete=fields.CASCADE
        )

        class Meta:
            table_name = 'books'

    db = await Database('__url__', models=[Writer, Book])

    async with db.acquire() as conn:
        await conn.create_table('books')

    # Assert the connection.
    asyncpg_conn.execute.assert_awaited_once_with(
        f'CREATE TABLE IF NOT EXISTS "books" ("title" VARCHAR(200), '
        '"date" TIMESTAMPTZ, "author" UUID REFERENCES "writers" ("pk") ON '
        'DELETE CASCADE)'
    )


@pytest.mark.asyncio
async def test_create_all_tables_1(asyncpg_conn):

    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Writer(Model):
        pk = fields.UUIDField(primary_key=True)
        full_name = fields.CharField(max_length=400)

        class Meta:
            table_name = 'writers'

    class Book(Model):
        title = fields.CharField(max_length=200)
        date = fields.DateTimeField()
        author = fields.ForeignKeyField(to='writers')

        class Meta:
            table_name = 'books'

    db = await Database('__url__', models=[Writer, Book])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    # Assert the connection.
    assert asyncpg_conn.execute.mock_calls == [
        call('CREATE TABLE IF NOT EXISTS "writers" '
             '("pk" UUID PRIMARY KEY, "full_name" VARCHAR(400))'),
        call(f'CREATE TABLE IF NOT EXISTS "books" ("title" VARCHAR(200), '
             '"date" TIMESTAMPTZ, "author" UUID REFERENCES "writers" ("pk"))'),
    ]


@pytest.mark.asyncio
async def test_models_with_base_model(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model

    class BaseModel(Model):
        pk = fields.UUIDField(primary_key=True)

        class Meta:
            abstract = True

    class Writer(BaseModel):
        class Meta:
            table_name = 'writers'

    class Book(BaseModel):
        author = fields.ForeignKeyField(to='writers')

    db = await Database('__url__', models=[Writer, Book])

    # Create the tables.
    async with db.acquire() as conn:
        await conn.create_all_tables()

    assert asyncpg_conn.execute.mock_calls == [
        call('CREATE TABLE IF NOT EXISTS "writers" '
             '("pk" UUID PRIMARY KEY)'),
        call(f'CREATE TABLE IF NOT EXISTS "book" ('
             '"pk" UUID PRIMARY KEY, '
             '"author" UUID REFERENCES "writers" ("pk"))'),
    ]


@pytest.mark.asyncio
async def test_select_multiple(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model

    pk1 = uuid4()
    pk2 = uuid4()

    asyncpg_conn.fetch.return_value = [
        {'text': 'h', 'pk': pk1},
        {'text': 'h', 'pk': pk2}
    ]
    asyncpg_conn.fetchval.return_value = 2

    class Model(Model):
        pk = fields.UUIDField(primary_key=True)
        text = fields.CharField(max_length=200)

    db = await Database('__url__', models=[Model])

    async with db.acquire() as conn:
        instances = await conn.select(Model).where(text='h')

    assert isinstance(instances[0], Model)
    assert isinstance(instances[1], Model)
    assert instances[0]['text'] == 'h'
    assert instances[1]['text'] == 'h'
    assert instances[0]['pk'] == pk1
    assert instances[1]['pk'] == pk2

    asyncpg_conn.fetchval.assert_awaited_once_with(
        'SELECT COUNT(*) FROM "model" WHERE "text"=$1', 'h'
    )

    asyncpg_conn.fetch.assert_awaited_once_with(
        'SELECT "pk", "text" FROM "model" WHERE "text"=$1', 'h'
    )


@pytest.mark.asyncio
async def test_select_from_model(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model

    pk = uuid4()

    asyncpg_conn.fetch.return_value = [{'text': 'hola', 'pk': pk}]
    asyncpg_conn.fetchval.return_value = 1

    class Model(Model):
        pk = fields.UUIDField(primary_key=True)
        text = fields.CharField(max_length=200)

    db = await Database('__url__', models=[Model])

    async with db.acquire() as conn:

        # Get one model.
        model = await conn.select(Model).where(text='hola').one()

    assert isinstance(model, Model), ".one should return the right instance."
    assert model['text'] == 'hola'
    assert 'pk' in model._data, "pk should be in _data"

    asyncpg_conn.fetchval.assert_awaited_once_with(
        'SELECT COUNT(*) FROM "model" WHERE "text"=$1', 'hola'
    )

    asyncpg_conn.fetch.assert_awaited_once_with(
        'SELECT "pk", "text" FROM "model" WHERE "text"=$1 LIMIT 1', 'hola'
    )


@pytest.mark.asyncio
async def test_select_one_empty_selection(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model
    import frankfurt.exceptions

    pk = uuid4()
    asyncpg_conn.fetchval.return_value = 0

    class Model(Model):
        pk = fields.UUIDField(primary_key=True)

    db = await Database('__url__', models=[Model])

    async with db.acquire() as conn:
        # Get one model.
        with pytest.raises(frankfurt.exceptions.EmptySelection):
            await conn.select(Model).where(pk=pk).one()

    asyncpg_conn.fetchval.assert_awaited_once_with(
        'SELECT COUNT(*) FROM "model" WHERE "pk"=$1', pk
    )


@pytest.mark.asyncio
async def test_select_one_multiple_rows(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model
    import frankfurt.exceptions

    pk = uuid4()
    asyncpg_conn.fetchval.return_value = 2

    class Model(Model):
        pk = fields.UUIDField(primary_key=True)

    db = await Database('__url__', models=[Model])

    async with db.acquire() as conn:
        # Get one model.
        with pytest.raises(frankfurt.exceptions.MultipleRowsSelected):
            await conn.select(Model).where(pk=pk).one()

    asyncpg_conn.fetchval.assert_awaited_once_with(
        'SELECT COUNT(*) FROM "model" WHERE "pk"=$1', pk
    )

@pytest.mark.asyncio
async def test_insert_model(asyncpg_conn):

    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Model(Model):
        pk = fields.UUIDField(primary_key=True)
        text = fields.CharField(max_length=200)

        class Meta:
            table_name = 'models'

    db = await Database('__url__', models=[Model])

    # Create a model.
    model = Model(text='hello!')

    # Set up the mock.
    asyncpg_conn.fetchrow.return_value = {
        'row': (model['pk'], 'hello!')
    }

    # Get a session.
    async with db.acquire() as conn:
        await conn.insert(model)

    asyncpg_conn.fetchrow.assert_awaited_once_with(
        'INSERT INTO "models" ("pk", "text") VALUES ($1, $2) '
        'RETURNING ("pk", "text")',
        model['pk'], "hello!"
    )


@pytest.mark.asyncio
async def test_update_model(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model, UpdateMixin

    pk = uuid4()
    asyncpg_conn.fetchrow.return_value = {
        'row': (pk, 'hello!', None)
    }

    class Model(Model, UpdateMixin):
        pk = fields.UUIDField(primary_key=True)
        text1 = fields.CharField(max_length=200)
        text2 = fields.CharField(max_length=200)

        class Meta:
            table_name = 'models'

    db = await Database('__url__', models=[Model])

    async with await db.acquire() as conn:

        # Create a model.
        model = Model(text1='hello!', pk=pk)

        # Explicit call to update.
        await conn.update(model)

    asyncpg_conn.fetchrow.assert_awaited_once_with(
        'UPDATE "models" SET "text1"=$1, "text2"=$2 WHERE "pk"=$3 '
        'RETURNING ("pk", "text1", "text2")',
        "hello!", None, pk
    )


@pytest.mark.asyncio
async def test_delete_model_prevent_full_table_delete(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model, DeleteMixin

    asyncpg_conn.fetch.return_value = {
        'text': 'hello!'
    }

    class Model(Model, DeleteMixin):
        pk = fields.UUIDField(primary_key=True)
        text1 = fields.CharField(max_length=200)
        text2 = fields.CharField(max_length=200)

        class Meta:
            table_name = 'models'

    db = await Database('__url__', models=[Model])

    async with db.acquire() as conn:

        # Create a model
        model = Model(text1='hello!')

        # Save the model assumes is an update.
        with pytest.raises(Exception):
            await conn.delete(model)

    asyncpg_conn.fetch.assert_not_awaited()


async def _test_delete_model(asyncpg_conn):
    from frankfurt import Database, fields
    from frankfurt.models import Model, DeleteMixin

    pk = uuid4()

    asyncpg_conn.fetch.return_value = {
        'row': (pk, 'hello!', None)
    }

    class Model(Model, DeleteMixin):
        pk = fields.UUIDField(primary_key=True)
        text1 = fields.CharField(max_length=200)
        text2 = fields.CharField(max_length=200)

        class Meta:
            table_name = 'models'

    db = await Database('__url__', models=[Model])

    return db, Model(text1='hello!', pk=pk), pk


@pytest.mark.asyncio
async def test_delete_model(asyncpg_conn):

    db, instance, pk = await _test_delete_model(asyncpg_conn)

    # Save the model assumes is an update.
    async with db.acquire() as conn:
        await conn.delete(instance)

    asyncpg_conn.fetch.assert_awaited_once_with(
        'DELETE FROM "models" WHERE "pk"=$1 '
        'RETURNING ("pk", "text1", "text2")', pk
    )


@pytest.mark.asyncio
async def test_delete_mixin(asyncpg_conn):

    db, instance, pk = await _test_delete_model(asyncpg_conn)

    # Save the model assumes is an update.
    async with db.acquire() as conn:
        await instance.delete(conn)

    asyncpg_conn.fetch.assert_awaited_once_with(
        'DELETE FROM "models" WHERE "pk"=$1 '
        'RETURNING ("pk", "text1", "text2")', pk
    )


@pytest.mark.asyncio
async def test_create_mixin(asyncpg_conn):

    # Set tup the result from fetchrow.
    pk = uuid4()
    asyncpg_conn.fetchrow.return_value = {
        'row': (pk, )
    }

    from frankfurt import Database, fields
    from frankfurt.models import Model, CreateMixin

    class Book(Model, CreateMixin):
        pk = fields.UUIDField(primary_key=True)

    # Start the database.
    db = await Database('__url__', models=(Book,))

    # Acquire a connection/session.
    conn = await db.acquire()

    # Create a book.
    await Book.create(conn, pk=pk)

    # Assert the calls to db.
    asyncpg_conn.fetchrow.assert_awaited_once_with(
        'INSERT INTO "book" ("pk") VALUES ($1) '
        'RETURNING ("pk")',
        pk
    )
