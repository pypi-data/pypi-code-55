from abc_storage.generators import users as users_gen
from abc_storage.generators import questions as questions_gen


async def create_entities(client, count: int = 1, **params):
    answers = []
    for i in range(count):
        resp, status = await users_gen.create_entities(client, **params)
        assert status == 201
        answer = {'primary_key': {}}
        answer['primary_key']['user_id'] = resp[0]['_id']
        resp, status = await questions_gen.create_entities(client, **params)
        assert status == 201
        answer['primary_key']['question_id'] = resp[0]['_id']
        answers.append(answer)
    return answers
