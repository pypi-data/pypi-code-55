import pytest

import tests

from abc_storage import generators
from abc_storage.clients.storage import user
from tests.client import data


user_1 = data.user_1
user_2 = data.user_2


@pytest.mark.asyncio
async def test_create_user_not_found_fields():
    await generators.clean_storage(tests.client_storage())

    method = user.Create([{}])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 422


@pytest.mark.asyncio
async def test_create_user():
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 201


@pytest.mark.asyncio
async def test_create_users():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1, user_2])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 201


@pytest.mark.asyncio
async def test_get_user():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, _ = await tests.client_storage().request(method)

    method = user.Get(args=[resp['_id']])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200
    assert '_id' in resp


@pytest.mark.asyncio
async def test_get_user_not_found():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Get(args=['1'])
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 404


@pytest.mark.asyncio
async def test_get_users():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    await tests.client_storage().request(method)
    method = user.Create([user_2])
    await tests.client_storage().request(method)

    method = user.GetAll()
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200
    assert len(resp['_items']) == 2


@pytest.mark.asyncio
async def test_get_users_empty():
    
    await generators.clean_storage(tests.client_storage())

    method = user.GetAll()
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200
    assert len(resp['_items']) == 0


@pytest.mark.asyncio
async def test_delete_users_not_found():
    await generators.clean_storage(tests.client_storage())

    method = user.DeleteAll()
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_delete_users():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    await tests.client_storage().request(method)

    method = user.DeleteAll()
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_delete_user():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, _ = await tests.client_storage().request(method)

    method = user.Delete(resp['_id'], resp['_etag'])
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_delete_user_not_found():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, _ = await tests.client_storage().request(method)

    resp['_id'] = resp['_id'][:-2] + ('00' if resp['_id'] != '00' else '01')
    method = user.Delete(resp['_id'], resp['_etag'])
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 204


@pytest.mark.asyncio
async def test_patch_user():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, _ = await tests.client_storage().request(method)

    method = user.Update(user=user_2, _id=resp['_id'], etag=resp['_etag'])
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 200


@pytest.mark.asyncio
async def test_patch_user_not_found():
    
    await generators.clean_storage(tests.client_storage())

    method = user.Create([user_1])
    resp, _ = await tests.client_storage().request(method)

    resp['_id'] = resp['_id'][:-2] + ('00' if resp['_id'] != '00' else '01')
    method = user.Update(user=user_2, _id=resp['_id'], etag=resp['_etag'], replace=False)
    
    resp, status_code = await tests.client_storage().request(method)
    assert status_code == 404

