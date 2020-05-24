import aiohttp
from discord import Client
import json

class EnjoyAPIException(Exception): pass

class EnjoyAPI:
    def __init__(self, bot: Client, token: str):

        """ Класс клиента """
        self.endpoint = 'https://api.enjoymickeybot.info'
        self.bot: Client = bot
        self.token: str = token
        if not hasattr(bot, 'session'):
            self.bot.session: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.bot.loop)
    


    async def check(self, userID: int):

        """ Получить данные от пользователя """
        if not userID: raise EnjoyAPIException('Не указан ID пользователя')

        async with self.bot.session.get(f'{self.endpoint}/check/{userID}', headers = { 'Authorization': self.token}) as res:
            res: aiohttp.ClientResponse
            if res.status not in [200, 404]: raise EnjoyAPIException(f'Призойшла внутреняя ошибка, статус: {res.status}')


            return await res.json(encoding='UTF-8')

        