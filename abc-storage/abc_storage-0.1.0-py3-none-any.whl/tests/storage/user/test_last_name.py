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
async def test_create_user_last_name_not_passed():
    last_name = None
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_empty():
    last_name = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_min_invalid():
    last_name = lambda: "1" * 0
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_valid_min_valid():
    last_name = lambda: "1" * 1
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_last_name_max_valid():
    last_name = lambda: "1" * 128
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_last_name_max_invalid():
    last_name = lambda: "1" * 129
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_integer_zero():
    last_name = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_integer_positive():
    last_name = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_integer_negative():
    last_name = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_float_zero():
    last_name = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_float_positive():
    last_name = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_float_negative():
    last_name = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_list():
    last_name = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_dict():
    last_name = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_bool_true():
    last_name = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_bool_false():
    last_name = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_last_name_nullable():
    last_name = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), last_name=last_name)
    assert status == 201
