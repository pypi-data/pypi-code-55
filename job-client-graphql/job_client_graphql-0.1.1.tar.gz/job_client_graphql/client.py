
import json
import logging
import asyncio

import datetime as dt

from urllib.parse import urlparse
from IPython.display import display, HTML

from .w_socket import WSocket
from .client_graphql_ws import ClientGraphqlWs
from .client_graphql_http import ClientGraphqlHttp
from .store import Store
from .util import Util
from .cell_display import CellDisplay

import nest_asyncio
nest_asyncio.apply()


class Client:
    """
    """

    def __init__(self,
                 server_url,
                 default_channel,
                 default_action=None,
                 password=None,
                 history_length=100,
                 pages={},
                 key=None,
                 alert=None,
                 debug=False,
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

        if self.ssl:
            uri_ws = server_url.replace('https', 'wss')
        else:
            uri_ws = server_url.replace('http', 'ws')
        self.client_gql_ws = ClientGraphqlWs(
            uri_ws,
            self.store,
            self.update,
            self.update_max_len,
            self.debug
        )

        uri_http = server_url
        self.client_gql_http = ClientGraphqlHttp(
            uri_http,
            self.debug
        )

        logging_level = logging.DEBUG if self.debug else False
        logger = logging.getLogger('asyncio')
        logger.setLevel(logging_level)
        logger.addHandler(logging.StreamHandler())

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
        return f'{channel}.{name}'

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

        query_string = """
        query ($password: String!) {
            checkPassword(password: $password) 
        }
        """
        variables = {
            "password": self.password,
        }

        res = self.client_gql_http.request(
            query_string,
            variables=variables
        )

        if not(res and res.get('checkPassword')):
            raise Exception('Invalid password')

    def read(self, name, channel=None):
        """
        """
        channel = channel or self.channel

        query_string = """
        query ($channel: String!, $name: String!) {
            read(channel: $channel, name: $name) {
                name
                value
            }
        }
        """
        variables = {
            "channel": channel,
            "name": name
        }

        res = self.client_gql_http.request(
            query_string,
            variables=variables
        )

        val = self._parse(res)
        val = val['read']
        if val:
            val = self._parse(val['value'])

        if not channel in self.store:
            self.store[channel] = Store(channel,
                                        action=self.action)
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

        query_string = """
        query ($channel: String!, $name: String!, $start: Int!, $end: Int!) {
            readHisto(channel: $channel, name: $name, start: $start, end: $end) {
                value
                timestamp
            }
        }
        """
        variables = {
            "channel": channel,
            "name": name,
            "start": start,
            "end": start + n-1,
        }

        res = self.client_gql_http.request(
            query_string,
            variables=variables
        )

        val = self._parse(res)
        val = val['readHisto']

        for e in val:
            e['value'] = self._parse(e['value'])

        if not timestamp:
            return [e['value'] for e in val]

        for e in val:
            e['timestamp'] = dt.datetime.fromisoformat(e['timestamp'])
        return val

    def write(self, name, value,
              channel=None, add_histo=True, expiry=None):
        """
        """
        channel = channel or self.channel

        if isinstance(value, (int, float)):
            value = str(value)

        query_string = """
        mutation ($channel: String!, $name: String!, $value: String, $add_histo: Boolean, $expiry: Int) {
            write(channel: $channel, name: $name, value: $value, add_histo: $add_histo, expiry: $expiry) {
                channel
                name
            }
        }
        """
        variables = {
            'channel': channel,
            'name': name,
            'value': value,
            'add_histo': add_histo,
            'expiry': expiry
        }

        res = self.client_gql_http.request(
            query_string,
            variables=variables
        )
        if res and res.get('write'):
            return True

        print(res)
        print(json.loads(res['raw'])['payload'].get('errors'))
        return False

    def publish(self, name, value, channel=None):
        """
        """
        channel = channel or self.channel

        if isinstance(value, (int, float)):
            value = str(value)

        query_string = """
        mutation ($channel: String!, $name: String!, $value: String) {
            publish(channel: $channel, name: $name, value: $value) {
                channel
                name
            }
        }
        """
        variables = {
            'channel': channel,
            'name': name,
            'value': value,
        }

        res = self.client_gql_http.request(
            query_string,
            variables=variables
        )
        if res and res.get('publish'):
            return True

        print(res)
        print(json.loads(res['raw'])['payload'].get('errors'))
        return False

    def publish_write(self, name, value,
                      channel=None, add_histo=True, expiry=None):
        """
        """
        channel = channel or self.channel

        if isinstance(value, (int, float)):
            value = str(value)

        query_string = """
        mutation ($channel: String!, $name: String!, $value: String, $add_histo: Boolean, $expiry: Int) {
            publishWrite(channel: $channel, name: $name, value: $value, add_histo: $add_histo, expiry: $expiry) {
                channel
                name
            }
        }
        """
        variables = {
            'channel': channel,
            'name': name,
            'value': value,
            'add_histo': add_histo,
            'expiry': expiry
        }

        res = self.client_gql_http.request(
            query_string,
            variables=variables
        )
        if res and res.get('publishWrite'):
            return True

        print(res)
        print(json.loads(res['raw'])['payload'].get('errors'))
        return False

    def subscribe(self,
                  channel=None,
                  action=None,
                  pattern=True,
                  test=lambda x: True):
        """
        """
        channel = channel or self.channel

        # self.action = action
        # self.store.action = action

        query_string = """
        subscription ($channel: String!, $pattern: Boolean) {
            subscribe(channel: $channel, pattern: $pattern) {
                name
                value
            }
        }
        """
        variables = {'channel': channel, 'pattern': pattern}
        subscription_name = 'subscribe'

        ref = self.client_gql_ws.subscribe(
            query_string,
            variables,
            subscription_name,
            action=action,
            test=test,
            headers=None,
        )
        return ref

    def subscribe_stop(self, ref):
        """
        """
        self.client_gql_ws.subscribe_stop(ref)

    def subscribe_auth(self):
        """
        """
        self.out_alert = CellDisplay(name='alert', max_lines=3)

        def callback_alert(channel, name, value):
            if channel != self.alert:
                return
            if name != 'new-token':
                return

            auth_data = self.read(self.key, self.alert)
            self.store['auth'] = auth_data

            self.write(self.key, None, self.alert, add_histo=False, expiry=1)

            id_providers = list(auth_data.keys())
            s = f'store updated with auth data from ID providers {id_providers}'
            self.out_alert.update(s, kind='text', append=True)
            

        self.ref_alert = self.subscribe(channel=self.alert, action=callback_alert)
        self.out_alert.display()
        self.out_alert.update('waiting for auth data...', kind='text')

    def stop_subscribe_auth(self, clear_display=True):
        """
        """
        self.subscribe_stop(self.ref_alert)
        if clear_display:
            self.out_alert.clear()
