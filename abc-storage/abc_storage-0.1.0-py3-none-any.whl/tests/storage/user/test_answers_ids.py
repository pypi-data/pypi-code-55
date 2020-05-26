import pytest

import tests

from abc_storage import generators
from abc_storage.generators import users as users_gen
from abc_storage.generators import answers as answers_gen
from abc_storage.generators import primary_key as primary_key_gen


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture():
    await generators.clean_storage(tests.client_storage())

    yield


@pytest.fixture(scope='function')
@pytest.mark.asyncio
async def fixture_deps():
    await generators.clean_storage(tests.client_storage())

    primary_key = await primary_key_gen.create_entities(tests.client_storage())
    pk = lambda: primary_key[0]['primary_key']
    answer = lambda: {'integer': 12345}
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=pk, answer=answer)
    assert status == 201

    yield resp


@pytest.mark.asyncio
async def test_create_user_answer_ids_not_passed():
    answer_ids = None
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_empty():
    answer_ids = lambda: ""
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_NOT_empty():
    answer_ids = lambda: "1" * 1
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_integer_zero():
    answer_ids = lambda: 0
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_integer_positive():
    answer_ids = lambda: 1
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_integer_negative():
    answer_ids = lambda: -1
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_float_zero():
    answer_ids = lambda: 0.
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_float_positive():
    answer_ids = lambda: 1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_float_negative():
    answer_ids = lambda: -1.1
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_list():
    answer_ids = lambda: []
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_answer_ids_list_one_id(fixture_deps):
    answer = fixture_deps
    answer_ids = lambda: [answer[0]['_id']]
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_answer_ids_list_two_ids(fixture_deps):
    answer = fixture_deps
    answer_ids = lambda: [answer[0]['_id'], answer[0]['_id']]
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 201


@pytest.mark.asyncio
async def test_create_user_answer_ids_invalid_id():
    answer_ids = lambda: ['123123']
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_not_matched_id(fixture_deps):
    answer = fixture_deps
    answer_ids = lambda: [answer[0]['primary_key']['user_id']]
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_dict():
    answer_ids = lambda: {}
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_bool_true():
    answer_ids = lambda: True
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_bool_false():
    answer_ids = lambda: False
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422


@pytest.mark.asyncio
async def test_create_user_answer_ids_nullable():
    answer_ids = lambda: None
    resp, status = await users_gen.create_entities(tests.client_storage(), answer_ids=answer_ids)
    assert status == 422
