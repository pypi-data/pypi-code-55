import pynng
import json
import trio
import fire

from xbbg import blp
from xbbg.io import logs

BROKDER_PORT = 9228


class DataFeeds(object):

    def __init__(self, pub, tickers, **kwargs):
        self.pub_port = pub
        self._pub_url_ = f'tcp://*'
        self.tickers = [tickers] if isinstance(tickers, str) else tickers
        self.data = dict()
        self._logger_ = logs.get_logger(DataFeeds, **kwargs)
        self._kwargs_ = kwargs

    async def run(self):

        pub_url = f'{self._pub_url_}:{self.pub_port}'
        self._logger_.info(f'Publishing to {pub_url} ...')

        with pynng.Pub0(listen=pub_url) as pub:
            for feed in blp.live(tickers=self.tickers, flds='LAST_PRICE', json=True):
                try:
                    self._logger_.debug(feed)
                    await pub.asend(json.dumps(feed).encode('utf-8'))
                except KeyboardInterrupt: break


def run_feeds(**kwargs):

    kwargs['log'] = kwargs.get('log', 'debug')
    if 'pub' not in kwargs: kwargs['pub'] = BROKDER_PORT
    if 'tickers' not in kwargs:
        kwargs['tickers'] = ['ESA Index', 'VIX Index']
        # kwargs['tickers'] = ['BABA US Equity', 'FXI US Equity']

    feeds = DataFeeds(**kwargs)
    trio.run(feeds.run)


if __name__ == '__main__':

    fire.Fire(run_feeds)
