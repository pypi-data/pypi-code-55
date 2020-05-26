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
async def test_create_user_active_not_passed():
    active = None
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_empty():
    active = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_NOT_empty():
    # TODO: Invalid test (problem with EVE). 422 must be
    active = lambda: "1" * 1
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_active_integer_zero():
    # TODO: Invalid test (problem with EVE). 422 must be
    active = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_active_integer_positive():
    # TODO: Invalid test (problem with EVE). 422 must be
    active = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_active_integer_negative():
    active = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_float_zero():
    active = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_float_positive():
    active = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_float_negative():
    active = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_list():
    active = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_dict():
    active = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_active_bool_true():
    active = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_active_bool_false():
    active = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_active_nullable():
    active = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), active=active)
    assert status == 422
