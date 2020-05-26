from abc_storage import generators as gen
from abc_storage.clients.storage import question


async def create_entities(client, count: int = 1, **params):
    default = {
        'title': lambda: gen.fake.first_name(),
        'block_type': lambda: 'integer',
        'text': lambda: gen.fake.phone_number(),
    }
    return await gen.random_entities(
        count=count, default_entity=default, params=params, client=client, method=lambda e: question.Create(e)
    )
