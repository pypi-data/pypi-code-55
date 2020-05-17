import pynng
import json
import trio
import fire

from xbbg.io import logs

BROKDER_PORT = 9224


class DataClient(object):

    def __init__(self, sub=BROKDER_PORT, **kwargs):

        self.sub_port = sub
        self.data = dict()
        self._sub_url_ = 'tcp://localhost'
        self._rep_port_ = 17
        self._logger_ = logs.get_logger(DataClient, **kwargs)

    async def start_sync(self):
        """
        Start syncing process so that messages won't lost
        """
        rep_port = self.sub_port + self._rep_port_
        with pynng.Req0(dial=f'{self._sub_url_}:{rep_port}') as req:
            await req.asend(f'READY: {rep_port}'.encode('utf-8'))
            self._logger_.debug(await req.arecv())
            await trio.sleep(.001)

    async def run(self):

        sub_url = f'{self._sub_url_}:{self.sub_port}'
        self._logger_.info(f'Subscribing to {sub_url} ...')

        with pynng.Sub0(dial=sub_url, recv_timeout=100) as sub:
            sub.subscribe(b'')
            # await self.start_sync()
            while True:
                try:
                    raw = await sub.arecv()
                    data = json.loads(raw.decode('utf-8'))
                    self._logger_.debug(data)
                    if isinstance(data, dict):
                        self.data.update(data)
                    # await trio.sleep(.02)
                except pynng.Timeout: pass
                except KeyboardInterrupt: break


def run_client(**kwargs):

    kwargs['log'] = kwargs.get('log', 'debug')
    dc = DataClient(**kwargs)
    trio.run(dc.run)


if __name__ == '__main__':

    fire.Fire(run_client)
