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
async def test_create_question_title_not_passed():
    title = None
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_empty():
    title = lambda: ""
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_min_invalid():
    title = lambda: "1" * 0
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_valid_min_valid():
    title = lambda: "1" * 1
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_title_max_valid():
    title = lambda: "1" * 256
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 201


@pytest.mark.asyncio
async def test_create_question_title_max_invalid():
    title = lambda: "1" * 257
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_integer_zero():
    title = lambda: 0
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_integer_positive():
    title = lambda: 1
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_integer_negative():
    title = lambda: -1
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_float_zero():
    title = lambda: 0.
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_float_positive():
    title = lambda: 1.1
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_float_negative():
    title = lambda: -1.1
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_list():
    title = lambda: []
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_dict():
    title = lambda: {}
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_bool_true():
    title = lambda: True
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_bool_false():
    title = lambda: False
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422


@pytest.mark.asyncio
async def test_create_question_title_nullable():
    title = lambda: None
    resp, status = await questions_gen.create_entities(tests.client_storage(), title=title)
    assert status == 422
