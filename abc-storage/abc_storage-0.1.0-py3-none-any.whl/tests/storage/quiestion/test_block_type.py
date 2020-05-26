import pytest

import tests

from abc_storage import generators
from abc_storage.generators import questions as questions_gen


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture():
    await generators.clean_storage(tests.client_storage())

    yield


@pytest.mark.asyncio
async def test_create_question_block_type_not_passed():
    block_type = None
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_empty():
    block_type = lambda: ""
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_invalid():
    block_type = lambda: "xxxxxxxxxxxxxxxxxxx"
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_integer():
    block_type = lambda: "integer"
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_block_type_float():
    block_type = lambda: "float"
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_block_type_opened():
    block_type = lambda: "opened"
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_block_type_closed():
    block_type = lambda: "closed"
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_block_type_integer_zero():
    block_type = lambda: 0
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_integer_positive():
    block_type = lambda: 1
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_integer_negative():
    block_type = lambda: -1
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_float_zero():
    block_type = lambda: 0.
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_float_positive():
    block_type = lambda: 1.1
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_float_negative():
    block_type = lambda: -1.1
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_list():
    block_type = lambda: []
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_dict():
    block_type = lambda: {}
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_bool_true():
    block_type = lambda: True
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_bool_false():
    block_type = lambda: False
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_block_type_nullable():
    block_type = lambda: None
    resp, status = await questions_gen.create_entities(tests.client_storage(), block_type=block_type)
    assert status == 422
