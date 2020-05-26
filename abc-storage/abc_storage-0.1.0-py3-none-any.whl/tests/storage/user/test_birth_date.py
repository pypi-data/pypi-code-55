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
async def test_create_user_birth_date_not_passed():
    birth_date = None
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_empty_string():
    # TODO: Invalid test (problem with EVE). 422 must be
    birth_date = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_birth_date_NOT_empty_string():
    birth_date = lambda: "1"
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_invalid_format_string():
    birth_date = lambda: "01-01-1970"
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_integer_zero():
    # TODO: Invalid test (problem with EVE). 422 must be
    birth_date = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_birth_date_integer_positive():
    birth_date = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_integer_negative():
    birth_date = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_float_zero():
    # TODO: Invalid test (problem with EVE). 422 must be
    birth_date = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_birth_date_float_positive():
    birth_date = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_float_negative():
    birth_date = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_list():
    # TODO: Invalid test (problem with EVE). 422 must be
    birth_date = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_birth_date_dict():
    # TODO: Invalid test (problem with EVE). 422 must be
    birth_date = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_birth_date_bool_true():
    birth_date = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_birth_date_bool_false():
    # TODO: Invalid test (problem with EVE). 422 must be
    birth_date = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_birth_date_nullable():
    birth_date = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), birth_date=birth_date)
    assert status == 201
