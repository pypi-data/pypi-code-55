#!/usr/bin/env python
#
# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""WSGI utility library tests."""
import six
from six.moves import filter

__author__ = 'rafe@google.com (Rafe Kaplan)'


import six.moves.http_client
import unittest

from protorpc import test_util
from protorpc import util
from protorpc import webapp_test_util
from protorpc.wsgi import util as wsgi_util

APP1 = wsgi_util.static_page('App1')
APP2 = wsgi_util.static_page('App2')
NOT_FOUND = wsgi_util.error(six.moves.http_client.NOT_FOUND)


class WsgiTestBase(webapp_test_util.WebServerTestBase):

  server_thread = None

  def CreateWsgiApplication(self):
    return None

  def DoHttpRequest(self,
                    path='/',
                    content=None,
                    content_type='text/plain; charset=utf-8',
                    headers=None):
    connection = six.moves.http_client.HTTPConnection('localhost', self.port)
    if content is None:
      method = 'GET'
    else:
      method = 'POST'
    headers = {'content=type': content_type}
    headers.update(headers)
    connection.request(method, path, content, headers)
    response = connection.getresponse()

    not_date_or_server = lambda header: header[0] not in ('date', 'server')
    headers = list(filter(not_date_or_server, response.getheaders()))

    return response.status, response.reason, response.read(), dict(headers)


class StaticPageBase(WsgiTestBase):

  def testDefault(self):
    default_page = wsgi_util.static_page()
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(200, status)
    self.assertEqual('OK', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testHasContent(self):
    default_page = wsgi_util.static_page('my content')
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(200, status)
    self.assertEqual('OK', reason)
    self.assertEqual('my content', content)
    self.assertEqual({'content-length': str(len('my content')),
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testHasContentType(self):
    default_page = wsgi_util.static_page(content_type='text/plain')
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(200, status)
    self.assertEqual('OK', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/plain',
                      },
                      headers)

  def testHasStatus(self):
    default_page = wsgi_util.static_page(status='400 Not Good Request')
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(400, status)
    self.assertEqual('Not Good Request', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testHasStatusInt(self):
    default_page = wsgi_util.static_page(status=401)
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(401, status)
    self.assertEqual('Unauthorized', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testHasStatusUnknown(self):
    default_page = wsgi_util.static_page(status=909)
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(909, status)
    self.assertEqual('Unknown Error', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testHasStatusTuple(self):
    default_page = wsgi_util.static_page(status=(500, 'Bad Thing'))
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(500, status)
    self.assertEqual('Bad Thing', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testHasHeaders(self):
    default_page = wsgi_util.static_page(headers=[('x', 'foo'),
                                                  ('a', 'bar'),
                                                  ('z', 'bin')])
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(200, status)
    self.assertEqual('OK', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                       'x': 'foo',
                       'a': 'bar',
                       'z': 'bin',
                      },
                      headers)

  def testHeadersUnicodeSafe(self):
    default_page = wsgi_util.static_page(headers=[('x', 'foo')])
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(200, status)
    self.assertEqual('OK', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                       'x': 'foo',
                      },
                      headers)
    self.assertTrue(isinstance(headers['x'], str))

  def testHasHeadersDict(self):
    default_page = wsgi_util.static_page(headers={'x': 'foo',
                                                  'a': 'bar',
                                                  'z': 'bin'})
    self.ResetServer(default_page)
    status, reason, content, headers = self.DoHttpRequest()
    self.assertEqual(200, status)
    self.assertEqual('OK', reason)
    self.assertEqual('', content)
    self.assertEqual({'content-length': '0',
                       'content-type': 'text/html; charset=utf-8',
                       'x': 'foo',
                       'a': 'bar',
                       'z': 'bin',
                      },
                      headers)


class FirstFoundTest(WsgiTestBase):

  def testEmptyConfiguration(self):
    self.ResetServer(wsgi_util.first_found([]))
    status, status_text, content, headers = self.DoHttpRequest('/')
    self.assertEqual(six.moves.http_client.NOT_FOUND, status)
    self.assertEqual(six.moves.http_client.responses[six.moves.http_client.NOT_FOUND], status_text)
    self.assertEqual(util.pad_string(six.moves.http_client.responses[six.moves.http_client.NOT_FOUND]),
                      content)
    self.assertEqual({'content-length': '512',
                       'content-type': 'text/plain; charset=utf-8',
                      },
                      headers)

  def testOneApp(self):
    self.ResetServer(wsgi_util.first_found([APP1]))

    status, status_text, content, headers = self.DoHttpRequest('/')
    self.assertEqual(six.moves.http_client.OK, status)
    self.assertEqual(six.moves.http_client.responses[six.moves.http_client.OK], status_text)
    self.assertEqual('App1', content)
    self.assertEqual({'content-length': '4',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testIterator(self):
    self.ResetServer(wsgi_util.first_found(iter([APP1])))

    status, status_text, content, headers = self.DoHttpRequest('/')
    self.assertEqual(six.moves.http_client.OK, status)
    self.assertEqual(six.moves.http_client.responses[six.moves.http_client.OK], status_text)
    self.assertEqual('App1', content)
    self.assertEqual({'content-length': '4',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

    # Do request again to make sure iterator was properly copied.
    status, status_text, content, headers = self.DoHttpRequest('/')
    self.assertEqual(six.moves.http_client.OK, status)
    self.assertEqual(six.moves.http_client.responses[six.moves.http_client.OK], status_text)
    self.assertEqual('App1', content)
    self.assertEqual({'content-length': '4',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testTwoApps(self):
    self.ResetServer(wsgi_util.first_found([APP1, APP2]))

    status, status_text, content, headers = self.DoHttpRequest('/')
    self.assertEqual(six.moves.http_client.OK, status)
    self.assertEqual(six.moves.http_client.responses[six.moves.http_client.OK], status_text)
    self.assertEqual('App1', content)
    self.assertEqual({'content-length': '4',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testFirstNotFound(self):
    self.ResetServer(wsgi_util.first_found([NOT_FOUND, APP2]))

    status, status_text, content, headers = self.DoHttpRequest('/')
    self.assertEqual(six.moves.http_client.OK, status)
    self.assertEqual(six.moves.http_client.responses[six.moves.http_client.OK], status_text)
    self.assertEqual('App2', content)
    self.assertEqual({'content-length': '4',
                       'content-type': 'text/html; charset=utf-8',
                      },
                      headers)

  def testOnlyNotFound(self):
    def current_error(environ, start_response):
      """The variable current_status is defined in loop after ResetServer."""
      headers = [('content-type', 'text/plain')]
      status_line = '%03d Whatever' % current_status
      start_response(status_line, headers)
      return []

    self.ResetServer(wsgi_util.first_found([current_error, APP2]))

    statuses_to_check = sorted(httplib.responses.keys())
    # 100, 204 and 304 have slightly different expectations, so they are left
    # out of this test in order to keep the code simple.
    for dont_check in (100, 200, 204, 304, 404):
      statuses_to_check.remove(dont_check)
    for current_status in statuses_to_check:
      status, status_text, content, headers = self.DoHttpRequest('/')
      self.assertEqual(current_status, status)
      self.assertEqual('Whatever', status_text)


if __name__ == '__main__':
  unittest.main()
