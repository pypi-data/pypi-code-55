import pytest
from mock import call


@pytest.mark.asyncio
async def test_simple_inheritance(asyncpg_conn):

    from frankfurt import Database, fields
    from frankfurt.models import Model

    class BaseModel(Model):
        pk = fields.UUIDField(primary_key=True)

        class Meta:
            abstract = True

    class Example1(BaseModel):
        text1 = fields.CharField(max_length=200)

    class Example2(BaseModel):
        text2 = fields.CharField(max_length=200)

    db = await Database('__url__', models=[Example1, Example2])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    assert asyncpg_conn.execute.await_args_list == [
        call('CREATE TABLE IF NOT EXISTS "example1" '
             '("pk" UUID PRIMARY KEY, "text1" VARCHAR(200))'),
        call('CREATE TABLE IF NOT EXISTS "example2" '
             '("pk" UUID PRIMARY KEY, "text2" VARCHAR(200))'),
    ]


def standard_multi_table_example():

    from frankfurt import fields
    from frankfurt.models import Model

    class BaseModel(Model):
        pk = fields.UUIDField(primary_key=True)

        class Meta:
            abstract = True

    class Figure(BaseModel):
        pass

    class Rect(Figure):

        height = fields.IntegerField(
            default=0, non_negative=True, not_null=True
        )

        width = fields.IntegerField(
            default=0, non_negative=True, not_null=True
        )

    class Circle(Figure):

        radius = fields.IntegerField(
            default=0, non_negative=True, not_null=True
        )

    return Figure, Rect, Circle


@pytest.mark.asyncio
async def test_multi_table_models(asyncpg_conn):

    from frankfurt import Database

    Figure, Rect, Circle = standard_multi_table_example()

    db = await Database('__url__', models=[Rect, Circle, Figure])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    assert asyncpg_conn.execute.await_args_list == [
        call('CREATE TABLE IF NOT EXISTS "figure" ('
             '"pk" UUID PRIMARY KEY)'),
        call('CREATE TABLE IF NOT EXISTS "rect" ('
             '"pk" UUID PRIMARY KEY REFERENCES "figure" ("pk"), '
             '"height" INTEGER NOT NULL, "width" INTEGER NOT NULL)'),
        call('CREATE TABLE IF NOT EXISTS "circle" ('
             '"pk" UUID PRIMARY KEY REFERENCES "figure" ("pk"), '
             '"radius" INTEGER NOT NULL)'),
    ]


@pytest.mark.asyncio
async def test_multi_table_instance_insert(asyncpg_conn):

    from frankfurt import Database

    Figure, Rect, Circle = standard_multi_table_example()

    db = await Database('__url__', models=[Rect, Circle, Figure])

    async with db.acquire() as conn:
        rect = Rect()

        assert rect['pk'] is not None

        await conn.insert(rect)


def standard_poly_example():

    from frankfurt import fields
    from frankfurt.models import Model

    class BaseModel(Model):
        pk = fields.UUIDField(primary_key=True)

        class Meta:
            abstract = True

    class Figure(BaseModel):
        shape = fields.CharField(max_length=100, not_null=True)

        class Meta:
            polymorphic_on = 'shape'
            polymorphic_identity = 'figure'

    class Rect(Figure):

        height = fields.IntegerField(
            default=0, non_negative=True, not_null=True
        )

        width = fields.IntegerField(
            default=0, non_negative=True, not_null=True
        )

        class Meta:
            polymorphic_identity = 'rect'

    class Circle(Figure):

        radius = fields.IntegerField(
            default=0, non_negative=True, not_null=True
        )

        class Meta:
            polymorphic_identity = 'circle'

    return Figure, Rect, Circle


@pytest.mark.asyncio
async def test_poly_models(asyncpg_conn):

    from frankfurt import Database

    Figure, Rect, Circle = standard_poly_example()

    db = await Database('__url__', models=[Rect, Circle, Figure])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    assert asyncpg_conn.execute.await_args_list == [
        call('CREATE TABLE IF NOT EXISTS "figure" ('
             '"pk" UUID PRIMARY KEY, '
             '"shape" VARCHAR(100) NOT NULL)'),
        call('CREATE TABLE IF NOT EXISTS "rect" ('
             '"pk" UUID PRIMARY KEY REFERENCES "figure" ("pk"), '
             '"shape" VARCHAR(100) NOT NULL, '
             '"height" INTEGER NOT NULL, "width" INTEGER NOT NULL)'),
        call('CREATE TABLE IF NOT EXISTS "circle" ('
             '"pk" UUID PRIMARY KEY REFERENCES "figure" ("pk"), '
             '"shape" VARCHAR(100) NOT NULL, '
             '"radius" INTEGER NOT NULL)'),
    ]

@pytest.mark.asyncio
async def test_poly_instance_insert(asyncpg_conn):

    from frankfurt import Database

    Figure, Rect, Circle = standard_poly_example()

    db = await Database('__url__', models=[Rect, Circle, Figure])

    async with db.acquire() as conn:
        rect = Rect(height=10, width=20)
        assert rect['pk'] is not None

        pk = rect['pk']

        await conn.insert(rect)

    assert asyncpg_conn.fetchrow.await_args_list == [
        call('INSERT INTO "figure" ("pk", "shape") VALUES ($1, $2) '
             'RETURNING ("pk", "shape")',
             pk, 'rect'),
        call('INSERT INTO "rect" ("pk", "shape", "height", "width") '
             'VALUES ($1, $2, $3, $4) '
             'RETURNING ("pk", "shape", "height", "width")',
             pk, 'rect', 10, 20)
    ]
