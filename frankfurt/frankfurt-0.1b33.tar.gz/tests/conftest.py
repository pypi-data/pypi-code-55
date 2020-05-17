import pytest
from mock import patch, MagicMock, AsyncMock


@pytest.fixture(scope='function')
def conn():
    p = patch('frankfurt.database.asyncpg.create_pool', new=AsyncMock())
    m = p.start()
    m.return_value.acquire = AsyncMock(return_value = MagicMock())
    conn = m.return_value.acquire.return_value
    conn.__aenter__.return_value = conn
    tr = AsyncMock()
    tr.start = AsyncMock()
    conn.transaction = MagicMock(return_value=tr)
    conn.execute = AsyncMock()
    conn.fetchrow = AsyncMock()
    conn.fetchval = AsyncMock()
    conn.fetch = AsyncMock()
    yield conn
    p.stop()


@pytest.fixture(scope='function')
def asyncpg_conn():
    p = patch('frankfurt.database.asyncpg.create_pool', new=AsyncMock())
    m = p.start()
    m.return_value.acquire = AsyncMock(return_value = MagicMock())
    conn = m.return_value.acquire.return_value
    conn.__aenter__.return_value = conn
    tr = AsyncMock()
    tr.start = AsyncMock()
    conn.transaction = MagicMock(return_value=tr)
    conn.execute = AsyncMock()
    conn.fetchrow = AsyncMock()
    conn.fetchval = AsyncMock()
    conn.fetch = AsyncMock()
    yield conn
    p.stop()



@pytest.fixture(scope='function')
def create_pool():
    p = patch('frankfurt.database.asyncpg.create_pool', new=AsyncMock())
    m = p.start()
    m.return_value.acquire = AsyncMock(return_value = MagicMock())
    conn = m.return_value.acquire.return_value
    conn.__aenter__.return_value = conn
    tr = AsyncMock()
    tr.start = AsyncMock()
    conn.transaction = MagicMock(return_value=tr)
    conn.execute = AsyncMock()
    conn.fetchrow = AsyncMock()
    conn.fetchval = AsyncMock()
    conn.fetch = AsyncMock()
    yield m
    p.stop()
