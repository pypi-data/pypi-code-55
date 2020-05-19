
import json
import logging
import asyncio
import threading

from .w_socket import WSocket
from .util import Util
from .store import Store

import nest_asyncio
nest_asyncio.apply()


class ClientGraphqlWs:
    """
    """

    def __init__(self,
                 uri,
                 store,
                 update,
                 update_max_len=100,
                 debug=False):
        """
        """
        self.store = store
        self.update = update
        self.debug = debug
        self.update_max_len = update_max_len

        self.ws = WSocket(uri, debug)
        self.sub_ref = {}

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
            return json.loads(res)['payload']['data']
        except:
            return {'raw': res}

    def subscribe(self,
                  query,
                  variables=None,
                  subscription_name='',
                  action=None,
                  test=lambda x: True,
                  headers=None):
        """
        """
        self.loop = asyncio.new_event_loop()
        coro = self._subscribe(query, variables, subscription_name, headers, action, test)
        task = self.loop.create_task(coro)
        ref = self.loop.run_until_complete(task)
        return ref

    def subscribe_stop(self, ref):
        """
        """
        self.loop = asyncio.new_event_loop()
        coro = self._subscribe_stop(ref)
        task = self.loop.create_task(coro)
        self.loop.run_until_complete(task)

    async def _conn_init(self, ws, headers=None):
        """
        """
        payload = {'headers': headers} if headers else {}
        data = {'type': 'connection_init', 'payload': payload}
        self._log('data', data)
        await ws.send(json.dumps(data))
        res = await ws.receive()
        self._log('res', res)

    async def _start(self, ws, payload):
        """
        """
        _id = Util.random_uuid()
        data = {'id': _id, 'type': 'start', 'payload': payload}
        self._log('data', data)
        await ws.send(json.dumps(data))
        return _id

    async def _stop(self, ws, _id, await_res=True):
        """
        """
        data = {'id': _id, 'type': 'stop'}
        self._log('data', data)
        await ws.send(json.dumps(data))
        if await_res:
            res = await ws.receive()
            self._log('res', res)

    async def _request(self, query, variables, headers=None):
        """
        """
        payload = {'query': query, 'variables': variables}

        async with self.ws as ws:
            await self._conn_init(ws, headers)
            _id = await self._start(ws, payload)
            res = await ws.receive()
            self._log('res', res)
            await self._stop(ws, _id)
            return res

    def _build_handler(self, channel, subscription_name, action, test):
        """
        """
        # if not channel in self.store:
        #     self.store[channel] = Store(channel, action=action)
        # else:
        #     self.store[channel].action = action

        if not channel in self.store:
            self.store[channel] = Store(channel)

        def handler(payload):
            try:
                data = payload['data'][subscription_name]
            except:
                self._log('ERROR', payload)
                return

            name = data.get('name')
            value = data.get('value')
            if action:
                action(channel, name, value)

            if test(name):
                self.store[channel][name] = value
                self.update.append((channel, name, value))

                if len(self.update) > self.update_max_len:
                    self.update = self.update[-self.update_max_len:]

                self._log(f'\tdone: {channel}\tname:{name}\tvalue:{value}')

        return handler

    async def _subscribe(self,
                         query,
                         variables,
                         subscription_name,
                         headers=None,
                         action=None,
                         test=lambda x: True
                         ):
        """
        """
        payload = {'query': query, 'variables': variables}
        channel = variables.get('channel')
        _handler = self._build_handler(channel, subscription_name, action, test)
        self._log('payload', payload)
        self._log('headers', headers)

        ref = Util.random_uuid()

        async def _run_sub():
            async with self.ws as ws:
                # self._sub_ws = ws
                await self._conn_init(ws, headers)
                _id = await self._start(ws, payload)
                self.sub_ref[ref] = {'ws': ws, 'id': _id}
                self._log('id', _id)
                # self._sub_id = _id
                while self._subscription_running:
                    res = await ws.receive()
                    dic = json.loads(res)
                    self._log('dic', dic)
                    # self._log('test id', _id == dic['id'])
                    if dic['type'] == 'error' or dic['type'] == 'complete':
                        self._log('last msg subscription', dic)
                        self._subscription_running = False
                    elif dic['type'] != 'ka' and dic['id'] == _id:
                        _handler(dic['payload'])
                self._log('done _run_sub')

        def loop_in_thread():
            thread_loop = asyncio.new_event_loop()
            thread_loop.run_until_complete(_run_sub())

        self._subscription_running = True
        self._thread = threading.Thread(target=loop_in_thread, args=())
        self._thread.start()

        return ref

    async def _subscribe_stop(self, ref):
        """
        """
        dic = self.sub_ref.get(ref)
        if dic:
            await self._stop(dic.get('ws'),
                             dic.get('id'),
                             await_res=False)
            self.sub_ref.pop(ref)
            print(f'subscription ref={ref} stopped')
        else:
            print(f'subscribe ref {ref} does not exist')
