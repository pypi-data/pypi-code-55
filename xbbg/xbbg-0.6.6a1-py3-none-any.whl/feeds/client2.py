import zmq
import trio
import fire

from xbbg.io import logs

BROKDER_PORT = 9227
ZMQ_PUB = getattr(zmq, 'PUB')
ZMQ_SUB = getattr(zmq, 'SUB')
ZMQ_NOB = getattr(zmq, 'NOBLOCK')


class DataClient(object):

    def __init__(self, sub=BROKDER_PORT, **kwargs):

        self.sub_port = sub
        self.data = dict()
        self._logger_ = logs.get_logger(DataClient, **kwargs)

    async def run(self):

        sub_url = f'tcp://localhost:{self.sub_port}'
        self._logger_.info(f'[{DataClient.__name__}] Subscribing to {sub_url} ...')

        with zmq.Context() as context:
            with context.socket(ZMQ_SUB) as sub:
                sub.connect(sub_url)
                sub.subscribe('')

                while True:
                    try:
                        topic, msg = sub.recv_pyobj(ZMQ_NOB)
                        self._logger_.debug(f'Topic: {topic} / Message: {msg}')
                    except zmq.Again: pass
                    except TimeoutError: pass
                    except KeyboardInterrupt: break


def run_client(**kwargs):

    kwargs['log'] = kwargs.get('log', 'debug')
    dc = DataClient(**kwargs)
    trio.run(dc.run)


if __name__ == '__main__':

    fire.Fire(run_client)
