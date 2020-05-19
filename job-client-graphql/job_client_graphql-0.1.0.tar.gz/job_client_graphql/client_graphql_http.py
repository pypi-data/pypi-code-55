
import json
import logging
import asyncio
import aiohttp

# import threading

# from .w_socket import WSocket
from .util import Util
# from .store import Store

import nest_asyncio
nest_asyncio.apply()


class ClientGraphqlHttp:
    """
    """

    def __init__(self,
                 uri,
                 debug=False):
        """
        """
        self.uri = uri
        self.debug = debug

        logging_level = logging.DEBUG if debug else False
        logger = logging.getLogger('asyncio')
        logger.setLevel(logging_level)
        logger.addHandler(logging.StreamHandler())

    def _log(self, name, obj=None):
        """
        """
        if self.debug:
            print('-'*20, name)
            if obj:
                print(obj)
                print('-'*20)

    def request(self,
                query,
                variables=None,
                headers=None):
        """
        query or mutation
        """
        # self.loop = asyncio.get_event_loop()
        self.loop = asyncio.get_event_loop()
        coro = self._request(query, variables, headers)
        task = self.loop.create_task(coro)
        res = self.loop.run_until_complete(task)
        # res = self.loop.run_until_complete(asyncio.gather(*[task]))
        self._log('res', res)
        try:
            return res.get('data')
        except:
            return {'raw': res}


    async def _request(self, query, variables, headers=None):
        """
        """

        payload = {'query': query, 'variables': variables}

        async with aiohttp.ClientSession() as session:
            async with session.post(self.uri, json=payload) as res:
                data = await res.json()
                return data
