import pytest

import tests

from abc_storage import generators
from abc_storage.clients.storage import question
from tests.client import data


questions_1 = data.questions_1
questions_2 = data.questions_2


@pytest.mark.asyncio
async def test_create_question_not_found_fields():
    await generators.clean_storage(tests.client_storage())

    method = question.Create([{}])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 422


@pytest.mark.asyncio
async def test_create_question():
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 201


@pytest.mark.asyncio
async def test_create_questions():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1, questions_2])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 201


@pytest.mark.asyncio
async def test_get_question():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    resp, status = await tests.client_storage().request(method)
    assert status == 201

    method = question.Get(args=[resp['_id']])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200
    assert '_id' in resp


@pytest.mark.asyncio
async def test_get_question_not_found():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Get(args=['1'])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 404


@pytest.mark.asyncio
async def test_get_questions():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    await tests.client_storage().request(method)
    method = question.Create([questions_2])
    await tests.client_storage().request(method)

    method = question.GetAll()
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200
    assert len(resp['_items']) == 2


@pytest.mark.asyncio
async def test_get_questions_empty():
    
    await generators.clean_storage(tests.client_storage())

    method = question.GetAll()
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200
    assert len(resp['_items']) == 0


@pytest.mark.asyncio
async def test_delete_questions_not_found():
    await generators.clean_storage(tests.client_storage())

    method = question.DeleteAll()
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_delete_questions():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    await tests.client_storage().request(method)

    method = question.DeleteAll()
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_delete_question():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    resp, _ = await tests.client_storage().request(method)

    method = question.Delete(resp['_id'], resp['_etag'])
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_delete_question_not_found():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    resp, _ = await tests.client_storage().request(method)

    resp['_id'] = resp['_id'][:-2] + ('00' if resp['_id'] != '00' else '01')
    method = question.Delete(resp['_id'], resp['_etag'])
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_patch_question():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    resp, _ = await tests.client_storage().request(method)

    method = question.Update(question=questions_2, _id=resp['_id'], etag=resp['_etag'])
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200


@pytest.mark.asyncio
async def test_patch_question_not_found():
    
    await generators.clean_storage(tests.client_storage())

    method = question.Create([questions_1])
    resp, _ = await tests.client_storage().request(method)

    resp['_id'] = resp['_id'][:-2] + ('00' if resp['_id'] != '00' else '01')
    method = question.Update(question=questions_2, _id=resp['_id'], etag=resp['_etag'], replace=False)
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 404

