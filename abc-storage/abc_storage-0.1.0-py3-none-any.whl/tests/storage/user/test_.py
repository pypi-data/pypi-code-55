import pytest

import tests

from abc_storage import generators
from abc_storage.generators import users as users_gen


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture():
    await generators.clean_storage(tests.client_storage())

    yield


@pytest.mark.asyncio
async def test_create_user_valid():
    resp, status = await users_gen.create_entities(tests.client_storage(), count=1)
    assert status == 201


@pytest.mark.asyncio
async def test_create_users_valid():
    resp, status = await users_gen.create_entities(tests.client_storage(), count=2)
    assert status == 201
