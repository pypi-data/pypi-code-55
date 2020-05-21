import sys
import logging
import json

import requests
import msal

from .tokencache import TokenCache
from ..utils import jdebug
from .deltaiterator import GenericDeltaIterator
from .exceptions import MgraphApiError
from .cache import Cache


class ApiArgs:
    cache = False
    purge_cache = False
    statedir = '.'
    debug = False
    v = False

    def __init__(self, args):
        if not args:
            return
        for key in ['cache', 'purge_cache', 'statedir', 'v', 'debug']:
            if key in args:
                setattr(self, key, getattr(args, key))


class MgraphBase:
    access_token = None
    params = None
    debug = False
    cache = None

    def __init__(self, params='config.json', database=None, args=None):
        self.params = json.load(open(params))
        self.database = database
        self.args = ApiArgs(args)

        keyfilename = self.params['private_key_file']
        if self.args.cache:
            self.cache = Cache(args)
            if self.args.purge_cache:
                self.cache.purge()

        # Create a preferably long-lived app instance which maintains a token cache.
        tokencache = TokenCache(self.args)
        self.app = msal.ConfidentialClientApplication(
            self.params["client_id"], authority=self.params["authority"],
            client_credential={"thumbprint": self.params["thumbprint"],
                               "private_key": open(keyfilename).read()
                               },
            token_cache=tokencache.cache
        )

    def enable_debug(self):
        self.args.debug = True

    def connect(self):
        # The pattern to acquire a token looks like this.
        result = None

        # Firstly, looks up a token from cache
        # Since we are looking for token for the current app, NOT for an end user,
        # notice we give account parameter as None.
        result = self.app.acquire_token_silent(
            self.params["scope"], account=None)

        if not result:
            logging.info(
                "No suitable token exists in cache. Let's get a new one from AAD.")
            result = self.app.acquire_token_for_client(
                scopes=self.params["scope"])

        if "access_token" in result:
            # Calling graph using the access token
            self.access_token = result['access_token']
            logging.info('Authorized.')
        else:
            logging.error(result.get("error"))
            logging.error(result.get("error_description"))
            # You may need this when reporting a bug
            logging.error(result.get("correlation_id"))
            raise MgraphApiError(result)

    def _assert_connected(self):
        if not self.access_token:
            self.connect()
        if not self.access_token:
            logging.error('No access_token available.')
            sys.exit(1)

    def _url(self, url):
        '''add endpoint to url if it has no complete protocol'''
        if url.startswith('/'):
            return self.params["endpoint"] + url
        return url

    def _generic_iterate(self, graph_data):
        '''private
        Support for paged results. See https://docs.microsoft.com/de-de/graph/paging
        '''
        while 'value' in graph_data:
            nextlink = None
            # "@odata.nextLink": "https://graph.microsoft.com/v1.0/users?$skiptoken=X%27...00%27"
            if "@odata.nextLink" in graph_data:
                nextlink = graph_data.get("@odata.nextLink")

            for val in graph_data['value']:
                yield val

            if nextlink:
                graph_data = self.get(nextlink)
            else:
                break

    def get(self, url, **kwargs):
        self._assert_connected()
        if kwargs:
            params = '&'.join([f"${k}={v}" for k, v in kwargs.items() if k])
            if params:
                params = '?' + params
        else:
            params = ''

        graph_data = requests.get(  # Use token to call downstream service
            self._url(url + params),
            headers={'Authorization': 'Bearer ' + self.access_token}, ).json()

        if self.args.debug:
            recordfile = 'log.json'
            with open(recordfile, 'a+') as fp:  # pylint: disable=invalid-name
                fp.write(f'# GET {url}\n')
                fp.write(json.dumps(graph_data, indent=2))
                fp.write('\n\n')

            logging.debug(f'GET {url} {params}')
            jdebug(graph_data, caller='get')

        if 'error' in graph_data:
            raise MgraphApiError(
                graph_data, f'MsGraph GET Error: {url}{params}')

        return graph_data

    def get_paged(self, url, **kwargs):
        '''
        iterator over all graph results. Supports @odata.nextLink paging
        '''
        return self.get_deltaiterator(url, **kwargs)

    def get_deltaiterator(self, url, deltalink=None, **kwargs):
        '''
        iterator over all graph results. Supports @odata.nextLink paging and maintains @odata.deltaLink for next call
        '''
        return GenericDeltaIterator(self, url, deltalink=deltalink, **kwargs)

    def get_binary(self, url, headers=None, fd=None):  # pylint: disable=invalid-name
        if headers is None:
            headers = {}
        headers.update({'Authorization': 'Bearer ' + self.access_token})
        response = requests.get(
            self._url(url),
            headers=headers)
        if self.args.debug:
            logging.debug(f'GET {url}')
        if response.status_code == requests.codes.ok:  # pylint: disable=no-member
            if fd:  # 4 MB, so we do not use too much memory here
                for chunk in response.iter_content(chunk_size=4096*1024):
                    logging.debug(f'chunk {len(chunk)}')
                    fd.write(chunk)
                return None
            return response.content
        else:
            logging.error(json.dumps(response.json()))
            raise MgraphApiError(response)
        return None

    def post(self, url, data=None):
        self._assert_connected()
        graph_data = requests.post(  # Use token to call downstream service
            self._url(url),
            json=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + self.access_token}, ).json()
        if self.args.debug:
            logging.debug(f'POST {url}')
            jdebug(graph_data, caller='post')
        if 'error' in graph_data:
            raise MgraphApiError(graph_data)
        return graph_data

    def post_paged(self, url, data=None):
        '''
        iterator over all graph results. Supports @odata.nextLink paging
        '''
        return self._generic_iterate(
            self.post(url, data=data)
        )

    def patch(self, url, data=None):
        self._assert_connected()

        graph_data = requests.patch(  # Use token to call downstream service
            self._url(url),
            json=data,
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + self.access_token}, ).json()
        if self.args.debug:
            logging.debug(f'PATCH {url}')
            jdebug(graph_data, caller='patch')
        if 'error' in graph_data:
            raise MgraphApiError(graph_data)
        return graph_data

    def delete(self, url):
        self._assert_connected()

        response = requests.delete(  # Use token to call downstream service
            self._url(url),
            headers={'Content-Type': 'application/json',
                     'Authorization': 'Bearer ' + self.access_token}, )
        if self.args.debug:
            logging.debug(f'DELETE {url}')
            jdebug(response.json(), caller='delete')
        if response.status_code != 204:  # pylint: disable=no-member
            raise MgraphApiError(response.json())
        return response
