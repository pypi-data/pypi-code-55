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
async def test_create_user_cell_phone_not_passed():
    cell_phone = None
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_empty():
    cell_phone = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_min_invalid():
    cell_phone = lambda: "1" * 4
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_valid_min_valid():
    cell_phone = lambda: "1" * 5
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_cell_phone_max_valid():
    cell_phone = lambda: "1" * 32
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_cell_phone_max_invalid():
    cell_phone = lambda: "1" * 33
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_integer_zero():
    cell_phone = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_integer_positive():
    cell_phone = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_integer_negative():
    cell_phone = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_float_zero():
    cell_phone = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_float_positive():
    cell_phone = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_float_negative():
    cell_phone = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_list():
    cell_phone = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_dict():
    cell_phone = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_bool_true():
    cell_phone = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_bool_false():
    cell_phone = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_cell_phone_nullable():
    cell_phone = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), cell_phone=cell_phone)
    assert status == 201
