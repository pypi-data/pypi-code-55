import pynng
import trio
import fire

from functools import partial
from xbbg.io import logs

BROKDER_PORT = 9224


async def pubsub_serv(pub, sub, **kwargs):

    while True:
        try:
            data = await sub.arecv()
            if 'logger' in kwargs: kwargs['logger'].debug(data)
            await pub.asend(data=data)
            await trio.sleep(kwargs.get('sleep', .0001))
        except pynng.Timeout: pass
        except KeyboardInterrupt: break


class Broker(object):

    def __init__(self, sub, pub=BROKDER_PORT, **kwargs):

        self.sub_port = sub
        self.pub_port = pub
        self._pub_url_ = f'tcp://*'
        self._sub_url_ = 'tcp://localhost'
        self._rep_port_ = 17

        self._logger_ = logs.get_logger(Broker, **kwargs)

    async def start_sync(self):
        """
        Start syncing process so that messages won't lost
        """
        rep_port = self.pub_port + self._rep_port_
        with pynng.Rep0(listen=f'{self._pub_url_}:{rep_port}') as rep:
            self._logger_.debug(await rep.arecv())
            await rep.asend(f'GO: {rep_port}'.encode('utf-8'))
            await trio.sleep(.001)

    async def run(self):

        if not self.sub_port: return

        pub_url = f'{self._pub_url_}:{self.pub_port}'
        self._logger_.info(f'Publishing to {pub_url} ...')
        pub = pynng.Pub0(listen=pub_url)

        subs = []
        for dial in self.sub_port:
            dial_url = f'{self._sub_url_}:{dial}'
            self._logger_.info(f'Subscribing to {dial_url} ...')
            sub = pynng.Sub0(dial=dial_url, recv_timeout=100)
            sub.subscribe(b'')
            subs.append(sub)

        await self.start_sync()
        try:
            while True:
                try:
                    async with trio.open_nursery() as nursery:
                        broker = partial(pubsub_serv, logger=self._logger_)
                        for sub in subs: nursery.start_soon(broker, pub, sub)
                except pynng.Timeout: pass
                except KeyboardInterrupt: break
        finally:
            pub.close()
            for sub in subs: sub.close()


def run_broker(**kwargs):

    if 'sub' not in kwargs: kwargs['sub'] = [9226, 9227, 9228]
    kwargs['log'] = kwargs.get('log', 'debug')
    brk = Broker(**kwargs)
    trio.run(brk.run)


if __name__ == '__main__':

    fire.Fire(run_broker)
