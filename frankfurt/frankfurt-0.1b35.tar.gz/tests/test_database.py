import pytest


@pytest.mark.asyncio
async def test_create_pool(create_pool):
    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Example(Model):
        text = fields.CharField(max_length=200)

    await Database('__url__', models=[Example])

    # Assert that asyncpg is called.
    create_pool.assert_awaited_once_with(dsn='__url__')


@pytest.mark.asyncio
async def test_conn(create_pool):
    from frankfurt import Database, fields
    from frankfurt.models import Model

    class Example(Model):
        text = fields.CharField(max_length=200)

    db = await Database('__url__', models=[Example])

    async with db.acquire() as conn:
        await conn.create_all_tables()

    conn._conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "example" ("text" VARCHAR(200))'
    )

    # The connection must be acquired and released.
    db._pool.acquire.assert_awaited_once_with()
    db._pool.release.assert_awaited_once_with(conn._conn)

    # The transaction should be commited.
    conn._tr.commit.assert_awaited_once_with()
