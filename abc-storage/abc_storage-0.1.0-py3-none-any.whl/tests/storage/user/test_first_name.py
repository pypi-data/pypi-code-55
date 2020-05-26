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
async def test_create_user_first_name_not_passed():
    first_name = None
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_empty():
    first_name = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_min_invalid():
    first_name = lambda: "1" * 0
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_valid_min_valid():
    first_name = lambda: "1" * 1
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_first_name_max_valid():
    first_name = lambda: "1" * 128
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_first_name_max_invalid():
    first_name = lambda: "1" * 129
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_integer_zero():
    first_name = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_integer_positive():
    first_name = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_integer_negative():
    first_name = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_float_zero():
    first_name = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_float_positive():
    first_name = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_float_negative():
    first_name = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_list():
    first_name = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_dict():
    first_name = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_bool_true():
    first_name = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_bool_false():
    first_name = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_first_name_nullable():
    first_name = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), first_name=first_name)
    assert status == 201
