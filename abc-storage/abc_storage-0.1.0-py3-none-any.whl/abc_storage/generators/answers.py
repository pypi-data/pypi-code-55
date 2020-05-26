from abc_storage import generators as gen
from abc_storage.clients.storage import answer


async def create_entities(client, count: int = 1, **params):
    default = {
        'primary_key': lambda: {},
        'answer': lambda: [],
    }
    return await gen.random_entities(
        count=count, default_entity=default, params=params, client=client, method=lambda e: answer.Create(e)
    )
