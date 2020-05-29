# copyright 2014-2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# cwclientlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# cwclientlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with cwclientlib. If not, see <https://www.gnu.org/licenses/>.

"""A CWProxy class wraps a CubicWeb repository.

>>> import cwproxy
>>> p = cwproxy.CWProxy('https://www.cubicweb.org')
>>> a = p.rql('Any X,T WHERE X is Project, X title T')
>>> print(a.json())
"""

import json
import requests
import hmac
import hashlib
from time import time, sleep
from datetime import datetime, date
from urllib import parse as urlparse
import ssl
from typing import List

from .builders import build_trinfo

if not getattr(ssl, 'HAS_SNI', False):
    try:
        import urllib3.contrib.pyopenssl
        urllib3.contrib.pyopenssl.inject_into_urllib3()
    except ImportError:
        pass

RQLIO_API = '1.0'


class SignedRequestAuth(requests.auth.AuthBase):
    """Auth implementation for CubicWeb with cube signedrequest"""

    HEADERS_TO_SIGN = ('Content-MD5', 'Content-Type', 'Date')

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret

    def __call__(self, req):
        content = b''
        if req.body:
            content = req.body
        if isinstance(content, str):
            content = content.encode('utf-8')
        req.headers['Content-MD5'] = hashlib.md5(content).hexdigest()
        content_to_sign = (
            req.method + req.url
            + ''.join(req.headers.get(field, '')
                      for field in self.HEADERS_TO_SIGN))
        content_signed = hmac.new(self.secret.encode('utf-8'),
                                  content_to_sign.encode('utf-8')).hexdigest()
        req.headers['Authorization'] = 'Cubicweb %s:%s' % (self.token_id,
                                                           content_signed)
        return req


def date_header_value() -> str:
    return datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


class RemoteValidationError(Exception):
    pass


class NoResultError(Exception):
    "CWProxy.find*() called but result set is empty"


class NoUniqueEntity(Exception):
    "CWProxy.find_one() called but result set contains more than one entity"


class TaskFailedError(Exception):
    pass


class CWProxy(object):
    """CWProxy: A simple helper class to ease building CubicWeb_
    clients. It allows to:

    * execute RQL_ queries remotely (using rqlcontroller_),
    * access instances that requires authentication (using signedrequest_).

.. _CubicWeb: http://www.cubicweb.org/
.. _RQL: http://docs.cubicweb.org/annexes/rql/language
.. _rqlcontroller: http://www.cubicweb.org/project/cubicweb-rqlcontroller/
.. _signedrequest: http://www.cubicweb.org/project/cubicweb-signedrequest/
    """

    def __init__(self, base_url: str, auth=None, verify=None, timeout=None):
        """Create a CWProxy connection object to the :base_url: cubicweb app.

        :param auth: can be provided to handle authentication. For a
          cubicweb application providing the signedrequest_ feature,
          one can use the SignedRequestAuth authentifier.

        :param verify: can be False to disable server certificate
          checking, or the path to a CA bundle file.

        """
        purl = urlparse.urlparse(base_url)
        # we do **not** want urls to be built with a double /, (e.g.
        # http://host// or http://host//basepath)
        path = purl.path.strip('/')
        if path:
            path = '{:s}/{:s}'.format(purl.netloc, path)
        else:
            path = purl.netloc
        self.base_url = (purl.scheme, path)
        self.auth = auth
        self.timeout = timeout
        self._ssl_verify = verify
        self._default_vid = 'jsonexport'  # OR 'ejsonexport'?
        self._base_url = urlparse.urlunparse(self.base_url +
                                             ('', None, None, None))

    def handle_request(self, method: str, path: str, **kwargs):
        """Construct a requests.Request and send it through this proxy.

        Arguments are that of requests.request() except for `path` which will
        be used to build a full URL using the base URL bound to this proxy.
        """
        msg = "handle_request() got unexpected keyword argument '{}'"
        for unexpected in ('url', 'auth'):
            if unexpected in kwargs:
                raise TypeError(msg.format(unexpected))
        url = self.build_url(path)
        kwargs['auth'] = self.auth
        kwargs.setdefault('headers', {}).update(
            {'Date': date_header_value()}
        )
        kwargs.setdefault('verify', self._ssl_verify)
        kwargs.setdefault('timeout', self.timeout)
        return requests.request(method, url, **kwargs)

    def build_url(self, path: str, query=None):
        """Build the URL to query from self.base_url and the given path

        :param path: can be a string or an iterable of strings; if it
            is a string, it can be a simple path, in which case the
            URL will be built from self.base_url + path, or it can be
            an "absolute URL", in which case it will be queried as is
            (the query argument is then ignored)

        :param query: can be a sequence of two-elements **tuples** or
            a dictionary (ignored if path is an absolute URL)

        """
        if query:
            query = urlparse.urlencode(query, doseq=True)
        if isinstance(path, (list, tuple)):
            path = '/'.join(path)
        if path.startswith(self._base_url):
            assert query is None
            return path
        return urlparse.urlunparse(self.base_url + (path, None, query, None))

    def get(self, path: str, query=None):
        """Perform a GET on the cubicweb instance

        :param path: the path part of the URL that will be GET
        :param query: can be a sequence of two-element tuples or a doctionnary
        """
        headers = {'Accept': 'application/json'}
        return self.handle_request('GET', path, params=query, headers=headers)

    def post(self, path: str, **data):
        """Perform a POST on the cubicweb instance

        :param path: the path part of the URL that will be GET
        :param **data: will be passed as the 'data' of the request
        """
        kwargs = {
            'headers': {'Accept': 'application/json'},
            'data': data,
        }
        if 'files' in data:
            kwargs['files'] = data.pop('files')
        return self.handle_request('POST', path, **kwargs)

    def post_json(self, path: str, payload):
        """Perform a POST on the cubicweb instance with application/json
        Content-Type.

        :param path: the path part of the URL that will be GET
        :param payload: native data to be sent as JSON (not encoded)
        """
        kwargs = {
            'headers': {'Accept': 'application/json'},
            'json': payload,
        }
        return self.handle_request('POST', path, **kwargs)

    def view(self, vid: str, **args):
        """Perform a GET on <base_url>/view with <vid> and <args>

        :param vid: the vid of the page to retrieve
        :param **args: will be used to build the query string of the URL
        """
        args['vid'] = vid
        return self.get('/view', args)

    def execute(self, rql: str, args=None):
        """CW connection's like execute method.

        :param rql: should be a unicode string or a plain ascii string
        :param args: are the optional parameters used in the query (dict)
        """
        return self.rqlio([(rql, args or {})]).json()[0]

    def rql(self, rql: str, path='view', **data):
        """Perform an urlencoded POST to /<path> with rql=<rql>

        :param rql: should be a unicode string or a plain ascii string
        (warning, no string formating is performed)
        :param path: the path part of the generated URL
        :param **data: the 'data' of the request
        """
        if rql.split()[0] in ('INSERT', 'SET', 'DELETE'):
            raise ValueError('You must use the rqlio() method to make '
                             'write RQL queries')

        if not data.get('vid'):
            data['vid'] = self._default_vid
        if path == 'view':
            data.setdefault('fallbackvid', '404')
        if rql:  # XXX may be empty?
            if not rql.lstrip().startswith('rql:'):
                # add the 'rql:' prefix to ensure given rql is considered has
                # plain RQL so CubicWeb won't attempt other interpretation
                # (e.g. eid, 2 or 3 word queries, plain text)
                rql = 'rql:' + rql
            data['rql'] = rql

        headers = {
            'Accept': 'application/json',
            'Date': date_header_value(),
        }
        params = {'url': self.build_url(path),
                  'headers': headers,
                  'verify': self._ssl_verify,
                  'auth': self.auth,
                  'data': data,
                  }
        return requests.post(**params)

    def rqlio(self, queries):
        """Multiple RQL for reading/writing data from/to a CW instance.

        :param queries: list of queries, each query being a couple (rql, args)

        Example::

          queries = [('INSERT CWUser U: U login %(login)s, U upassword %(pw)s',
                      {'login': 'babar', 'pw': 'cubicweb rulez & 42'}),
                     ('INSERT CWGroup G: G name %(name)s',
                      {'name': 'pachyderms'}),
                     ('SET U in_group G WHERE G eid %(g)s, U eid %(u)s',
                      {'u': '__r0', 'g': '__r1'}),
                     ('INSERT File F: F data %(content)s, F data_name %(fn)s',
                      {'content': BytesIO('some binary data'),
                       'fn': 'toto.bin'}),
                    ]
          self.rqlio(queries)

        """
        headers = {
            'Accept': 'application/json',
            'Date': date_header_value(),
        }
        files = self.preprocess_queries(queries)

        params = {'url': self.build_url(('rqlio', RQLIO_API)),
                  'headers': headers,
                  'verify': self._ssl_verify,
                  'auth': self.auth,
                  'files': files,
                  }
        posted = requests.post(**params)
        if posted.status_code == 500:
            try:
                cause = posted.json()
            except Exception as exc:
                raise RemoteValidationError('%s (%s)', exc, posted.text)
            else:
                if 'reason' in cause:
                    # was a RemoteCallFailed
                    raise RemoteValidationError(cause['reason'])
        return posted

    def preprocess_queries(self, queries):
        """Pre process queries arguments to replace binary content by
        files to be inserted in the multipart HTTP query

        :param queries: list of queries, each query being a couple (rql, args)

        Any value that have a read() method will be threated as
        'binary content'.

        In the RQL query, binary value are replaced by unique '__f<N>'
        references (the ref of the file object in the multipart HTTP
        request).
        """

        files = {}
        for query_idx, (rql, args) in enumerate(queries):
            if args is None:
                continue
            for arg_idx, (k, v) in enumerate(args.items()):
                if hasattr(v, 'read') and callable(v.read):
                    # file-like object
                    fid = args[k] = '__f%d-%d' % (query_idx, arg_idx)
                    files[fid] = v
                elif isinstance(v, (date, datetime)):
                    args[k] = v.isoformat()
        files['json'] = ('json', json.dumps(queries), 'application/json')
        return files

    def _set_rql_request(self, rql_request: str, kwargs, sep=',') -> str:
        args = ['X {property_name:s} %({property_name:s})s'.format(
            property_name=property_name) for property_name in kwargs]
        if args:
            rql_request = u'{:s}{:s} {:s}'.format(
                rql_request, sep, ', '.join(args))
        return rql_request

    def _rql_args_query(self, rql_request: str, kwargs, sep=',') -> list:
        rql_request = self._set_rql_request(rql_request, kwargs, sep)
        response = self.rqlio([(rql_request, kwargs)])
        response.raise_for_status()
        results = response.json()
        return [row[0] for row in results[0]]

    def count(self, entity_type: str, **kwargs) -> int:
        """Return number of entities with the given type and
        properties in a CW instance.

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values
        :return: number of entities
        :rtype: int

        Example::

          >>> self.count('CWUser')
          3
          >>> self.count('CWUser', login='rms')
          1

        """
        rql_query = 'Any COUNT('
        rql_query += '1' if kwargs else 'X'
        rql_query += ') WHERE X is {:s}'.format(entity_type)
        return int(self._rql_args_query(rql_query, kwargs)[0])

    def exist(self, entity_type: str, **kwargs) -> bool:
        """Return true if there is at least one entity with the given type and
        properties in a CW instance and false otherwise.

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values
        :return: whether such an entity exists
        :rtype: boolean

        Example::

          >>> self.exist('CWUser', login='toto')
          False

        """
        rql_query = 'Any '
        rql_query += '1' if kwargs else 'X'
        rql_query += ' LIMIT 1 WHERE X is {:s}'.format(entity_type)
        try:
            return bool(self._rql_args_query(rql_query, kwargs))
        except RemoteValidationError as e:
            if 'unknown entity type {:s}'.format(entity_type) in str(e):
                return False
            raise e

    def find(self, entity_type: str, **kwargs) -> List[int]:
        """Return eid(s) of entitie(s) with the given type and properties in a
        CW instance.

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values
        :return: list of eid(s)
        :rtype: list

        Example::

          >>> self.find('CWUser')
          [20, 21]
          >>> self.find('CWUser', login='admin')
          [20]
        """
        return self._rql_args_query(
            'Any X WHERE X is {:s}'.format(entity_type), kwargs)

    def find_one(self, entity_type: str, **kwargs) -> int:
        """Return eid of the unique entity with the given type and properties
        in a CW instance. If there is none or multiple, it throws an exception
        that indicates the problem (NoResultError or NoUniqueEntity).

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values
        :return: eid
        :rtype: integer
        :raises NoResultError: there was no matching entity
        :raises NoUniqueEntity: there was multiple matching entities

        Example::

          >>> self.find_one('CWUser', login='admin')
          20
        """
        eids = self._rql_args_query(
            'Any X LIMIT 2 WHERE X is {:s}'.format(entity_type), kwargs)
        if len(eids) == 0:
            raise NoResultError('No result for {:s}'.format(entity_type))
        if len(eids) > 1:
            raise NoUniqueEntity('Cannot find unique {:s}'.format(entity_type))
        return eids[0]

    def find_last_created(self, entity_type: str, **kwargs) -> int:
        """Return eid of the last created entity with the given type and
        properties in a CW instance. If there is none, it throws an exception
        that indicates the problem (NoResultError).

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values
        :return: eid
        :rtype: integer
        :raises NoResultError: there was no matching entity

        Example::

          >>> self.find_last_created('CWUser')
          20
          >>> self.find_last_created('Blog', title='MyBlog')
          22
        """
        eid = self._rql_args_query(
            'Any X ORDERBY D DESC LIMIT 1 '
            'WHERE X is {:s}, X creation_date D'.format(entity_type), kwargs)
        if not eid:
            raise NoResultError('No result for {:s}'.format(entity_type))
        return eid[0]

    def get_state(self, eid: int) -> str:
        """Return name of the state of the entity with the given eid or nothing
        if the eid does not exist or if the entity with the given eid has no
        state.

        :param eid: eid of an entity
        :return: the name of the state (if one)
        :rtype: str

        Example::

          >>> self.get_state(1001)
          'wfs_finished'
        """
        response = self.rqlio([
            ('Any SN LIMIT 1 WHERE E eid %(eid)s, E in_state S, S name SN',
             {'eid': eid})
        ])
        response.raise_for_status()
        rset = response.json()
        if rset and rset[0] and rset[0][0]:
            return rset[0][0][0]
        return None

    def wait_for_status(self, eid: int, status,
                        timeout=60, timesleep=1) -> None:
        """Wait that the entity with given eid to be in status given. If it is
        not the case after timeout, a related exception is raised. The state is
        fetched and checked, then it sleeps if it is not yet the status given.

        :param eid: eid of an entity with a state
        :param status: status to wait for
        :param timeout: maximum time to wait for given status
        :param timesleep: time between each status fetch
        :raises TaskFailedError: status given was not failed and it failed
        :raises TimeoutError: timeout has expired

        Example::

          >>> self.wait_for_status(30, 'wfs_finished')
        """
        start_time = int(time())
        while True:
            sleep(timesleep)
            current_status = self.get_state(eid)
            if current_status == status:
                break
            if current_status == 'wfs_failed':
                raise TaskFailedError(eid)
            if int(time()) - start_time >= timeout:
                raise TimeoutError(eid)

    def wait_for_finish(self, eid: int, *args, **kwargs) -> None:
        """Wait that the entity with given eid to be in status finished. If it
        is not the case after timeout, a related exception is raised. The state
        is fetched and checked, then it sleeps if it is not yet in the status
        finished.

        :param eid: eid of an entity with a state
        :param timeout: maximum time to wait for given status
        :param timesleep: time between each status fetch
        :raises TaskFailedError: the task failed according to state
        :raises TimeoutError: timeout has expired

        Example::

          >>> self.wait_for_finish(30)
        """
        return self.wait_for_status(eid, 'wfs_finished', *args, **kwargs)

    def change_state(self, eid: int, status: str):
        """Try to change the state with the one given for the entity that have
        the given eid.

        :param eid: eid of an entity with a state
        :param status: new status to set

        Example::

          >>> self.change_state(30, 'wft_start')
        """
        return self.rqlio([build_trinfo(eid, status)])

    def insert(self, entity_type: str, **kwargs):
        """Insert an entity of the given type with given values of attributes.

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values

        Example::

          >>> self.insert('Project', name='start-up nation', author='Macron')
        """
        return self._rql_args_query(
            'INSERT {:s} X: '.format(entity_type), kwargs, '')

    def insert_if_not_exist(self, entity_type, **kwargs):
        """Insert an entity of the given type with given values of attributes
        if it does not already exist.

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values

        Example::

          >>> self.insert_if_not_exist('Project', name='cwclientlib')
        """
        if not self.exist(entity_type, **kwargs):
            return self.insert(entity_type, **kwargs)

    def delete(self, entity_type: str, **kwargs):
        """Delete all entities that have the given type
        and with given values of attributes.

        :param entity_type: entity type name
        :param kwargs: list of properties with associated values

        Example::

          >>> self.delete('Project', name='start-up nation', author='Macron')
        """
        return self._rql_args_query(
            'DELETE {:s} X WHERE '.format(entity_type), kwargs, '')
