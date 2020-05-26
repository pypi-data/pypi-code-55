import pytest

import tests

from abc_storage import generators
from abc_storage.generators import answers as answers_gen
from abc_storage.generators import primary_key as primary_key_gen


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture():
    await generators.clean_storage(tests.client_storage())

    yield


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture_deps():
    await generators.clean_storage(tests.client_storage())

    primary_key = await primary_key_gen.create_entities(tests.client_storage())

    yield primary_key[0]


@pytest.mark.asyncio
async def test_create_answer_primary_key_not_passed(fixture):
    primary_key = None
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_empty(fixture):
    primary_key = lambda: ""
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_min_invalid(fixture):
    primary_key = lambda: "11111"
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_integer_zero(fixture):
    primary_key = lambda: 0
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_integer_positive(fixture):
    primary_key = lambda: 1
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_integer_negative(fixture):
    primary_key = lambda: -1
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_float_zero(fixture):
    primary_key = lambda: 0.
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_float_positive(fixture):
    primary_key = lambda: 1.1
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_float_negative(fixture):
    primary_key = lambda: -1.1
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_list(fixture):
    primary_key = lambda: []
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_dict(fixture):
    primary_key = lambda: {}
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_valid_primary_key(fixture_deps):
    answers = fixture_deps
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 201


@pytest.mark.asyncio
async def test_create_answer_primary_key_invalid_another_question_id(fixture_deps):
    answers = fixture_deps
    answers['primary_key']['question_id'] = answers['primary_key']['user_id']
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_invalid_another_user_id(fixture_deps):
    answers = fixture_deps
    answers['primary_key']['question_id'] = answers['primary_key']['user_id']
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_invalid_another_question_id(fixture_deps):
    answers = fixture_deps
    answers['primary_key']['user_id'] = answers['primary_key']['question_id']
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_duplicate(fixture_deps):
    answers = fixture_deps
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 201
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_invalid_question_id(fixture_deps):
    answers = fixture_deps
    prefix = answers['primary_key']['question_id'][-4:]
    answers['primary_key']['question_id'] = prefix + ('0001' if prefix == '0000' else '0000')
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_invalid_user_id(fixture_deps):
    answers = fixture_deps
    prefix = answers['primary_key']['user_id'][-4:]
    answers['primary_key']['user_id'] = prefix + ('0001' if prefix == '0000' else '0000')
    primary_key = lambda: answers['primary_key']
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_bool_true(fixture):
    primary_key = lambda: True
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_bool_false(fixture):
    primary_key = lambda: False
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answer_primary_key_nullable(fixture):
    primary_key = lambda: None
    resp, status = await answers_gen.create_entities(tests.client_storage(), primary_key=primary_key)
    assert status == 422
