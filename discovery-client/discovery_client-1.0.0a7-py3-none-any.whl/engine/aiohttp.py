from discovery.engine.abc import Engine


class AioEngine(Engine):
    def __init__(self, *args, session=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = session

    async def get(self, *args, **kwargs):
        response = await self._session.get(*args, **kwargs)
        return response

    async def put(self, *args, **kwargs):
        response = await self._session.put(*args, **kwargs)
        return response

    async def delete(self, *args, **kwargs):
        response = await self._session.delete(*args, **kwargs)
        return response

    async def post(self, *args, **kwargs):
        response = await self._session.post(*args, **kwargs)
        return response

    @property
    def session(self):
        return self._session
