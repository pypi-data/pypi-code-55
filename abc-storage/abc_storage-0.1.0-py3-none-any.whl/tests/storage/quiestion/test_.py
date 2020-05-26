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
async def test_create_question_valid():
    resp, status = await questions_gen.create_entities(tests.client_storage(), count=1)
    assert status == 201


@pytest.mark.asyncio
async def test_create_questions_valid():
    resp, status = await questions_gen.create_entities(tests.client_storage(), count=2)
    assert status == 201
