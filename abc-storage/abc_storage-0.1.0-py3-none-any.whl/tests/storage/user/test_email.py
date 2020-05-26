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
async def test_create_user_email_not_passed():
    email = None
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_empty():
    email = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_min_invalid():
    email = lambda: "1" * 4
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_valid_min_valid():
    email = lambda: "1" * 5
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_email_max_valid():
    email = lambda: "1" * 256
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_email_max_invalid():
    email = lambda: "1" * 257
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_integer_zero():
    email = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_integer_positive():
    email = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_integer_negative():
    email = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_float_zero():
    email = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_float_positive():
    email = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_float_negative():
    email = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_list():
    email = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_dict():
    email = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_bool_true():
    email = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_bool_false():
    email = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_email_nullable():
    email = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), email=email)
    assert status == 201
