from abc_storage import generators as gen
from abc_storage.clients.storage import user
from abc_storage.schema import datetime


async def create_entities(client, count: int = 1, **params):
    default = {
        'first_name': lambda: gen.fake.first_name(),
        'last_name': lambda: gen.fake.last_name(),
        'cell_phone': lambda: gen.fake.phone_number(),
        'birth_date': lambda: gen.fake.date_object().strftime(datetime.datetime),
        'email': lambda: gen.fake.email(),
        'auth_hash': lambda: str(gen.fake.binary(20)),
        'active': lambda: gen.fake.pybool(),
        'answer_ids': lambda: [],
    }
    return await gen.random_entities(
        count=count, default_entity=default, params=params, client=client, method=lambda e: user.Create(e)
    )
