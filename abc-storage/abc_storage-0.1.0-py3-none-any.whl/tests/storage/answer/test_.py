import pytest

import tests

from abc_storage import generators
from abc_storage.generators import users as users_gen


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture():
    await generators.clean_storage(tests.client_storage())
    user, status = await users_gen.create_entities(tests.client_storage(), count=1)
    assert status == 201
    question, status = await users_gen.create_entities(tests.client_storage(), count=1)
    assert status == 201

    yield user, question


@pytest.mark.asyncio
async def test_create_user_valid(fixture):
    user, question = fixture
    user_id = lambda: user[0]['_id']
    question_id = lambda: question[0]['_id']
    resp, status = await users_gen.create_entities(tests.client_storage(), count=1, user_id=user_id,
                                                   question_id=question_id)
    assert status == 201


@pytest.mark.asyncio
async def test_create_users_valid(fixture):
    user, question = fixture
    user_id = lambda: user[0]['_id']
    question_id = lambda: question[0]['_id']
    resp, status = await users_gen.create_entities(tests.client_storage(), count=2, user_id=user_id,
                                                   question_id=question_id)
    assert status == 201
