import pytest
from mock import AsyncMock


@pytest.mark.asyncio
async def test_create_table_no_columns():
    import frankfurt.sql

    conn = AsyncMock()

    await frankfurt.sql.PartialCreateTable(
        table_name='test'
    ).execute(conn=conn)

    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "test"'
    )


@pytest.mark.asyncio
async def test_create_table_with_many_columns():
    import frankfurt.sql

    conn = AsyncMock()

    columns = {
        'col_0': frankfurt.sql.ColumnClause('dt_0'),
        'col_1': frankfurt.sql.ColumnClause('dt_1')
    }

    ct = frankfurt.sql.PartialCreateTable(table_name='test')
    ct.columns(**columns)
    await ct.execute(conn=conn)

    conn.execute.assert_called_once_with(
        'CREATE TABLE IF NOT EXISTS "test" ("col_0" dt_0, "col_1" dt_1)'
    )


@pytest.mark.asyncio
async def test_simple_insert():
    import frankfurt.sql

    conn = AsyncMock()
    conn.fetchrow.return_value = {
        'row': (1, 2)
    }

    ins = frankfurt.sql.PartialInsert(table_name='test')
    ins.values(a=1)
    ins.returning('a', 'b')

    record = await ins.execute(conn=conn)

    assert record['a'] == 1
    assert record['b'] == 2

    conn.fetchrow.assert_called_with(
        'INSERT INTO "test" ("a") VALUES ($1) RETURNING ("a", "b")', 1
    )


@pytest.mark.asyncio
async def test_delete_full_table():
    import frankfurt.sql

    conn = AsyncMock()

    # Define.
    delete = frankfurt.sql.PartialDelete(table_name="table")

    # Execute on await.
    await delete.execute(conn=conn)

    conn.fetch.assert_awaited_once_with(
        'DELETE FROM "table"'
    )


@pytest.mark.asyncio
async def test_delete_where():
    import frankfurt.sql

    conn = AsyncMock()

    # Define.
    delete = frankfurt.sql.PartialDelete(table_name="table")
    delete.where(pk=1, text="hola")

    # Execute on await.
    await delete.execute(conn=conn)

    # Assert for where values.
    conn.fetch.assert_awaited_once_with(
        'DELETE FROM "table" WHERE "pk"=$1 AND "text"=$2', 1, 'hola'
    )
