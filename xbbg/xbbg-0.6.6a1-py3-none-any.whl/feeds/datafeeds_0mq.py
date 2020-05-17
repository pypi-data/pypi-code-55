import zmq
import fire
import time

from xbbg.io import logs

ZMQ_PUB = getattr(zmq, 'PUB')
ZMQ_SUB = getattr(zmq, 'SUB')
ZMQ_NOB = getattr(zmq, 'NOBLOCK')


class DataFeeds(object):

    def __init__(self, pub, univ, **kwargs):

        self.pub_port = pub
        self.univ = univ
        self.data = dict()
        self._logger_ = logs.get_logger(DataFeeds, **kwargs)

    def run(self):

        pub_url = f'tcp://*:{self.pub_port}'
        self._logger_.info(f'[{DataFeeds.__name__}] Publishing to {pub_url} ...')

        sub_url = f'tcp://localhost:{self.pub_port}'
        self._logger_.info(f'[{DataFeeds.__name__}] Subscribing to {sub_url} ...')

        with zmq.Context() as context:
            with context.socket(ZMQ_PUB) as pub:
                pub.bind(pub_url)
                for d in [
                        'init', {('9988 HK', 'BID'): 210.2},
                        {'9988 HK': 211.0}, {'9988 HK': 211.4}
                ]:
                    self._logger_.debug(f'Sending {d} ...')
                    pub.send_pyobj(['', d])
                    time.sleep(.05)

            # with context.socket(ZMQ_SUB) as sub:
            #     sub.connect(sub_url)
            #     sub.subscribe('')
            #     while True:
            #         try:
            #             self._logger_.debug(sub.recv_pyobj(ZMQ_NOB))
            #             time.sleep(.05)
            #         except zmq.Again: pass
            #         except TimeoutError: pass
            #         except KeyboardInterrupt: break


def run_feeds(**kwargs):

    kwargs['log'] = kwargs.get('log', 'debug')
    if 'pub' not in kwargs: kwargs['pub'] = 9227
    if 'univ' not in kwargs: kwargs['univ'] = []
    feeds = DataFeeds(**kwargs)
    feeds.run()


if __name__ == '__main__':

    fire.Fire(run_feeds)
