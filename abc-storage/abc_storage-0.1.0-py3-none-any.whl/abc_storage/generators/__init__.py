import faker
from clients import http

from faker.providers import person, internet, python, phone_number, lorem, date_time

import abc_storage
from abc_storage.clients.storage import user, question, answer


fake = faker.Faker("ru_RU")
fake.add_provider(person)
fake.add_provider(internet)
fake.add_provider(python)
fake.add_provider(lorem)
fake.add_provider(phone_number)
fake.add_provider(date_time)


async def clean_storage(client):
    """
    clean storage

    :param client:
    :return:
    """
    methods = [
        user.DeleteAll(),
        question.DeleteAll(),
        answer.DeleteAll(),
    ]
    for m in methods:
        await client.request(m)


def __default_params(p, k, v):
    if k not in p:
        return v()
    if p[k] is None:
        return None
    return p[k]()


async def update_entities(client, method, name: str, entities: list):
    """
    update_entities updates entities

    :param client:
    :param method:
    :param name: name of argument of method (for example: block, class_ or other)
    :param entities: entities for update
    :return:
    """
    resps = []
    codes = []
    for e in entities:
        _id = e['_id']
        _etag = e['_etag']
        e = abc_storage.filter_meta_fields([e])[0]
        m = method(_id=_id, etag=_etag, **{name: e})
        resp, status_code = await client.request(m)
        codes.append(status_code)
        resps.append({'_id': resp['_id'], '_etag': resp['_etag']})
    return resps, codes


def __clean_object(obj, resp):
    return {**resp, **{'_id': obj['_id'], '_etag': obj['_etag']}}


async def random_entities(count: int, default_entity: dict, params: dict, client: http.Client, method):
    """
    random_entities generates random entities by default values and by params. You pass default values and after that
    values from params dict will replace

    count must be more 0

    :param count: count object with current configuration
    :param default_entity:
    :param params:
    :param client:
    :param method: this is factory (callback) for creating from clients.Method
    :return:
    """
    assert count > 0
    entities = []
    for i in range(count):
        entity = {}
        for k, v in default_entity.items():
            if k in params and params[k] is None:
                continue
            v = __default_params(p=params, k=k, v=v)
            entity[k] = v
        entities.append(entity)
    resps, status_code = await client.request(method(entities))
    if status_code // 100 != 2:
        return resps, status_code
    if len(entities) == 1:
        resps = [resps]
    else:
        resps = resps['_items']
    resps = [__clean_object(obj, resp) for resp, obj in zip(entities, resps)]
    return resps, status_code


async def assert_count(client: http.Client, method: http.Method, count: int):
    """
    assert_count checks amount values in response (we check '_items' field from response)

    :param client:
    :param method:
    :param count:
    :return:
    """
    resps, status_code = await client.request(method)
    assert status_code == 200
    if '_items' in resps:
        assert len(resps['_items']) == count
        return
    assert len(resps) == count


def assert_status_codes(status_codes: list, code: int):
    """
    assert_status_codes checks status codes

    :param status_codes:
    :param code:
    :return:
    """
    for s in status_codes:
        assert s == code
