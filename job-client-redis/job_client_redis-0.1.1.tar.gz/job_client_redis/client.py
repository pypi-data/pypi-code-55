
import json
import redis
import threading

import datetime as dt

from urllib.parse import urlparse
from IPython.display import display, HTML
from redis import AuthenticationError

from .store import Store


class Client:
    """
    """

    def __init__(self,
                 server_url,
                 default_channel,
                 redis_host='localhost',
                 redis_port=6379,
                 default_action=None,
                 password=None,
                 history_length=100,
                 pages={},
                 key=None,
                 alert=None,
                 debug=False,
                 db=0,
                 ):
        """
        """
        self.channel = default_channel
        self.debug = debug
        self.update_max_len = history_length
        self.action = default_action
        self.password = password
        self.pages = pages
        self.key = key
        self.alert = alert

        self.store = Store('top', action=self.action)
        self.update = []

        self.ssl = server_url.startswith('https')
        o = urlparse(server_url)
        self.host = o.hostname
        self.port = o.port
        self.path = o.path

        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=self.password)

        self.pubsub = self.r.pubsub()

        self.debug = debug
        self.histo_sep = '|'
        self.thread = None

        self.check_password()
        self.set_pages()

    def set_pages(self, pages=None):
        """
        """
        pages = self.pages or pages

        if isinstance(pages, str) and pages.startswith('http'):
            try:
                r = rq.get(pages)
            except:
                raise Exception(f'Cannot load {pages}')

            try:
                self.pages = r.json()
                print(f'loaded pages from {pages}')
            except:
                raise Exception(f'Cannot json.load {pages}')

        elif isinstance(pages, dict):
            self.pages = pages

    def build_url(self, page_name):
        """
        """
        url = self.pages.get(page_name)

        if not url:
            print(f'no url for page_name {page_name}')
            return

        qs = f'?host={self.host}&port={self.port}&path={self.path}&ssl={self.ssl}'

        if self.channel:
            qs += f'&channel={self.channel}'
        if self.key:
            qs += f'&key={self.key}'
        if self.alert:
            qs += f'&alert={self.alert}'

        url += qs

        return url

    def show_btn_page(self, page_name):
        """
        """
        url = self.build_url(page_name)

        if not url:
            return

        style_btn = """
        background-color:light-grey;
        width: 200px;
        """
        style_sep = """
        margin-right: 20px;;
        """
        func_copy = f"""
            const el = document.createElement('textarea');
            el.value = `{url}`;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
        """
        html = f"""
        <div style="display: flex; align-items: center">
            <div style="{style_sep}">Page <span style="color:red;">{page_name.upper()}</span></div>
            <button style="{style_btn}{style_sep}" onclick="window.open('{url}', '_blank'); return false;">Open in new tab</button>
            <button style="{style_btn}" onclick="{func_copy}">Copy url to clipboard </button>
        </div>
        """

        display(HTML(html))

    def _build_key(self, channel, name):
        """
        """
        return f'{channel}:{name}'

    def _parse(self, value):
        """
        """
        if isinstance(value, list):
            return [self._parse(e) for e in value]

        if isinstance(value, bytes):
            value = value.decode('utf-8')
        try:
            val = json.loads(value)
        except:
            val = value
        return val

    def _stringify(self, value):
        """
        """
        if isinstance(value, str):
            return value
        return json.dumps(value)

    def check_password(self):
        """
        """
        if not self.password:
            return True

        try:
            self.r.set('foo-bar-baz', 'test')
            return True
        except AuthenticationError:
            print('invalid password')
            return False

    def read(self, name, channel=None):
        """
        """
        channel = channel or self.channel

        key = self._build_key(channel, name)
        value = self.r.get(key)
        val = self._parse(value)

        if not channel in self.store:
            self.store[channel] = Store(channel,
                                        action=self.store.action)

        self.store[channel][name] = val
        self.update.append((channel, name, val))

        if len(self.update) > self.update_max_len:
            self.update = self.update[-self.update_max_len:]

        return val

    def read_histo(self, name, n=10, start=0,
                   channel=None, timestamp=False):
        """
        """
        channel = channel or self.channel
        key = self._build_key(channel, name + self.histo_sep + 'histo')
        value = self.r.lrange(key, start, start + n-1)
        val = self._parse(value)

        if not timestamp:
            return [e['value'] for e in val]

        for e in val:
            e['timestamp'] = dt.datetime.fromisoformat(e['timestamp'])
        return val

    def write(self, name, value, channel=None, add_histo=True, expiry=None):
        """
        """
        channel = channel or self.channel

        key = self._build_key(channel, name)
        string = self._stringify(value)

        if add_histo:
            key_histo = key + self.histo_sep + 'histo'
            ts = dt.datetime.now().isoformat()
            self.r.lpush(key_histo, self._stringify({
                'value': string,
                'timestamp': ts
            }))

        self.r.set(key, string, ex=expiry)

        return True

    def publish(self, name, value, channel=None):
        """
        """
        channel = channel or self.channel

        string = self._stringify(value)
        dic = {'name': name, 'value': string}
        self.r.publish(channel, self._stringify(dic))

        return True

    def publish_write(self, name, value, channel=None, add_histo=True, expiry=None):
        """
        """
        channel = channel or self.channel

        self.publish(name, value, channel)
        self.write(name, value, channel, add_histo=add_histo, expiry=expiry)

        return True

    def _build_handler(self, channel, action, test):
        """
        """
        if not channel in self.store:
            self.store[channel] = Store(channel, action=action)
        else:
            self.store[channel].action = action

        def handler(msg):
            if self.debug:
                m = json.loads(msg['data'].decode('utf-8'))
                print(f'update channel\n\traw: {m}')

            data = msg['data'].decode('utf-8')
            dic = json.loads(data)
            name, value = dic['name'], dic['value']

            if test(name):
                self.store[channel][name] = value
                self.update.append((channel, name, value))

                if len(self.update) > self.update_max_len:
                    self.update = self.update[-self.update_max_len:]

                if self.debug:
                    print(f'\tdone: {channel}\tname:{name}\tvalue:{value}')

        return {channel: handler}

    def subscribe(self,
                  channel=None,
                  action=None,
                  pattern=True,
                  test=lambda x: True):
        """
        """
        h_channel = channel or self.channel
        h_action = action or self.action

        dic_handler = self._build_handler(
            h_channel,
            h_action,
            test,
        )

        if pattern:
            self.pubsub.subscribe(**dic_handler)
        else:
            self.pubsub.psubscribe(**dic_handler)

        self.thread = self.pubsub.run_in_thread(sleep_time=0.02)

    def subscribe_stop(self):
        """
        """
        if self.thread:
            self.thread.stop()
