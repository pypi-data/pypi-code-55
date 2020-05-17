import pytest


def test_types():
    from frankfurt import fields

    f = fields.IntegerField()
    f.assert_type(1)
    f.assert_type(0)
    f.assert_type(-1)
    f.assert_type(None)

    f = fields.IntegerField(not_null=True)
    f.assert_type(1)
    f.assert_type(0)
    f.assert_type(-1)
    with pytest.raises(TypeError):
        f.assert_type(None)

    f = fields.IntegerField(non_negative=True)
    f.assert_type(1)
    f.assert_type(0)
    with pytest.raises(TypeError):
        f.assert_type(-1)
    f.assert_type(None)

    f = fields.IntegerField(non_negative=True)
    f.assert_type(1)
    f.assert_type(0)
    with pytest.raises(TypeError):
        f.assert_type(-1)
    f.assert_type(None)


def test_general_arguments():
    from frankfurt import fields

    with pytest.raises(TypeError):
        fields.UUIDField(pk=True)


@pytest.mark.asyncio
async def test_fields_by_examples(asyncpg_conn):

    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Example_1(Model):
        password = fields.BinaryField()

    db = await Database('__url__', models=[Example_1])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    asyncpg_conn.execute.assert_awaited_once_with(
        'CREATE TABLE IF NOT EXISTS "example_1" ("password" BYTEA)'
    )


def test_default_values():

    from frankfurt import fields
    from frankfurt.models import Model

    class Example(Model):
        text_1 = fields.CharField(max_length=200, default='text')
        text_2 = fields.CharField(max_length=200, default=None)
        text_3 = fields.CharField(max_length=200, default=lambda : "sentinel")

    example = Example()
    assert example['text_1'] == 'text'
    assert example['text_2'] is None
    assert example['text_3'] == 'sentinel'


def test_not_null_values():

    from frankfurt import fields
    from frankfurt.models import Model

    class Example(Model):
        text = fields.CharField(max_length=200, not_null=True)

    example = Example()

    with pytest.raises(KeyError):
        assert example['text'] is None


@pytest.mark.asyncio
async def test_unique_constraint(asyncpg_conn):

    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Example(Model):
        token = fields.CharField(max_length=64, unique=True)

    db = await Database('__url__', models=[Example])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    asyncpg_conn.execute.assert_awaited_once_with(
        'CREATE TABLE IF NOT EXISTS "example" ("token" VARCHAR(64) UNIQUE)'
    )
