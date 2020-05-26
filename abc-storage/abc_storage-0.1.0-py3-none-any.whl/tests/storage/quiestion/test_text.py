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
async def test_create_question_text_not_passed():
    text = None
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_empty():
    text = lambda: ""
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_min_invalid():
    text = lambda: "1" * 0
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_valid_min_valid():
    text = lambda: "1" * 1
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_text_max_valid():
    text = lambda: "1" * 65536
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_text_max_invalid():
    text = lambda: "1" * 65537
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_integer_zero():
    text = lambda: 0
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_integer_positive():
    text = lambda: 1
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_integer_negative():
    text = lambda: -1
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_float_zero():
    text = lambda: 0.
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_float_positive():
    text = lambda: 1.1
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_float_negative():
    text = lambda: -1.1
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_list():
    text = lambda: []
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_dict():
    text = lambda: {}
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_bool_true():
    text = lambda: True
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_bool_false():
    text = lambda: False
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_text_nullable():
    text = lambda: None
    resp, status = await questions_gen.create_entities(tests.client_storage(), text=text)
    assert status == 422
