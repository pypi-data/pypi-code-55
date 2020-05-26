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
async def test_create_user_auth_hash_not_passed():
    auth_hash = None
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_empty():
    auth_hash = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_min_invalid():
    auth_hash = lambda: "1" * 31
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_valid_min_valid():
    auth_hash = lambda: "1" * 32
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_auth_hash_max_valid():
    auth_hash = lambda: "1" * 4096
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_auth_hash_max_invalid():
    auth_hash = lambda: "1" * 4097
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_integer_zero():
    auth_hash = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_integer_positive():
    auth_hash = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_integer_negative():
    auth_hash = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_float_zero():
    auth_hash = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_float_positive():
    auth_hash = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_float_negative():
    auth_hash = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_list():
    auth_hash = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_dict():
    auth_hash = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_bool_true():
    auth_hash = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_bool_false():
    auth_hash = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_auth_hash_nullable():
    auth_hash = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), auth_hash=auth_hash)
    assert status == 422
