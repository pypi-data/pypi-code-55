import copy

import pytest

import tests

from abc_storage import generators
from abc_storage.clients.storage import question, user, answer
from tests.client import data


answer_1 = copy.deepcopy(data.answer)
answer_2 = copy.deepcopy(data.answer)
user_1 = copy.deepcopy(data.user_1)
user_2 = copy.deepcopy(data.user_2)
questions_1 = data.questions_1


@pytest.fixture(autouse=True, scope='function')
@pytest.mark.asyncio
async def fixture():
    global answer_1
    global answer_2
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201
    answer_1['primary_key']['user_id'] = resp['_id']

    method = question.Create([questions_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201
    answer_1['primary_key']['question_id'] = resp['_id']

    method = user.Create([user_2])
    resp, status = await tests.client_storage().request(method)
    assert status == 201
    answer_2['primary_key']['user_id'] = resp['_id']

    method = question.Create([questions_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201
    answer_2['primary_key']['question_id'] = resp['_id']

    yield


@pytest.mark.asyncio
async def test_create_answer():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201


@pytest.mark.asyncio
async def test_create_answer_not_found_fields():
    method = answer.Create([{}])
    resp, status = await tests.client_storage().request(method)
    assert status == 422


@pytest.mark.asyncio
async def test_create_answers():
    method = answer.Create([answer_1, answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201


@pytest.mark.asyncio
async def test_get_answer():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    method = answer.Get(args=[resp['_id']])
    resp, status = await tests.client_storage().request(method)
    assert status == 200
    assert '_id' in resp


@pytest.mark.asyncio
async def test_get_answer_not_found():
    method = answer.Get(args=['1'])
    resp, status = await tests.client_storage().request(method)
    assert status == 404


@pytest.mark.asyncio
async def test_get_answers():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201
    method = answer.Create([answer_2])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    method = answer.GetAll()
    resp, status = await tests.client_storage().request(method)
    assert status == 200
    assert len(resp['_items']) == 2


@pytest.mark.asyncio
async def test_get_answers_empty():
    method = answer.GetAll()
    resp, status = await tests.client_storage().request(method)
    assert status == 200
    assert len(resp['_items']) == 0


@pytest.mark.asyncio
async def test_delete_answers_not_found():
    method = answer.DeleteAll()
    
    resp, status = await tests.client_storage().request(method)
    assert status == 204


@pytest.mark.asyncio
async def test_delete_answers():
    method = answer.Create([answer_1])
    _, status = await tests.client_storage().request(method)
    assert status == 201

    method = answer.DeleteAll()
    
    resp, status = await tests.client_storage().request(method)
    assert status == 204


@pytest.mark.asyncio
async def test_delete_answer():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    method = answer.Delete(resp['_id'], resp['_etag'])
    
    resp, status = await tests.client_storage().request(method)
    assert status == 204


@pytest.mark.asyncio
async def test_delete_answer_not_found():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    resp['_id'] = resp['_id'][:-2] + ('00' if resp['_id'] != '00' else '01')
    method = answer.Delete(resp['_id'], resp['_etag'])
    
    resp, status = await tests.client_storage().request(method)
    assert status == 204


@pytest.mark.asyncio
async def test_patch_answer():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    method = answer.Update(answer=answer_1, _id=resp['_id'], etag=resp['_etag'])
    
    resp, status = await tests.client_storage().request(method)
    assert status == 200


@pytest.mark.asyncio
async def test_patch_answer_not_found():
    method = answer.Create([answer_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    resp['_id'] = resp['_id'][:-2] + ('00' if resp['_id'] != '00' else '01')
    method = answer.Update(answer=answer_1, _id=resp['_id'], etag=resp['_etag'], replace=False)
    
    resp, status = await tests.client_storage().request(method)
    assert status == 404

