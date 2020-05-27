import os
import time
import click
import random
from DalBaseUnit import DalBaseUnit

import sys
import copy
import json
import six
import traceback
import tornado.ioloop
import tornado.httputil
import tornado.httpclient

from tornado import gen
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from requests import cookies
from requests.cookies import MockRequest

class MockResponse(object):

    def __init__(self, headers):
        self._headers = headers

    def info(self):
        return self

    def getheaders(self, name):
        """make cookie python 2 version use this method to get cookie list"""
        return self._headers.get_list(name)

    def get_all(self, name, default=None):
        """make cookie python 3 version use this instead of getheaders"""
        if default is None:
            default = []
        return self._headers.get_list(name) or default


def extract_cookies_to_jar(jar, request, response):
    req = MockRequest(request)
    res = MockResponse(response)
    jar.extract_cookies(res, req)

class Fetcher:
    #todo, support self agent
    #user_agent = "pyspider/%s (+http://pyspider.org/)" % pyspider.__version__
    user_agent = ""
    allowed_options = ['method', 'data', 'connect_timeout', 'timeout', 'cookies', 'use_gzip', 'validate_cert']
    default_options = {
        'method': 'GET',
        'headers': {
        },
        'use_gzip': True,
        'timeout': 120,
        'connect_timeout': 20,
    }
    phantom_js_proxy = None
    splash_endpoint = None
    # splash_lua_source = open('./splash_fetcher.lua').read()

    def __init__(self):
        """
        port is determined by UnitRunFrame
        :param port: xmlrpc server port
        """
        self.http_client = tornado.httpclient.HTTPClient()

    def fetch_web(self, task):
        url = task['url']
        type = 'None'
        start_time = time.time()
        print("Fetch web url: {}".format(url))
        if 'fetch_type' in task:
            fetch_type = task['fetch_type']
        else:
            fetch_type = 'http'
        try:
            if fetch_type == 'phantomjs':
                result = self.phantom_js_fetch(url, task)
            elif fetch_type == 'splash':
                result = self.splash_fetch(url, task)
            else:
                result = self.http_fetch(url, task)
        except Exception as e:
            result = self.handle_error(type, url, task, start_time, e)
        return result

    def pack_tornado_request_parameters(self, url, task):
        fetch = copy.deepcopy(self.default_options)
        fetch['url'] = url
        fetch['headers'] = tornado.httputil.HTTPHeaders(fetch['headers'])
        fetch['headers']['User-Agent'] = self.user_agent
        task_fetch = task.get('craw_config', {})
        for each in self.allowed_options:
            if each in task_fetch:
                fetch[each] = task_fetch[each]
        fetch['headers'].update(task_fetch.get('headers', {}))

        if task.get('track'):
            track_headers = tornado.httputil.HTTPHeaders(
                task.get('track', {}).get('fetch', {}).get('headers') or {})
            track_ok = task.get('track', {}).get('process', {}).get('ok', False)
        else:
            track_headers = {}
            track_ok = False
        # proxy
        proxy_string = None
        if 'proxy' in task_fetch:
            if isinstance(task_fetch.get('proxy'), six.string_types):
                proxy_string = task_fetch['proxy']
            elif self.proxy and task_fetch.get('proxy', True):
                proxy_string = self.proxy
        if proxy_string:
            if '://' not in proxy_string:
                proxy_string = 'http://' + proxy_string
            proxy_splited = urlsplit(proxy_string)
            fetch['proxy_host'] = proxy_splited.hostname
            if proxy_splited.username:
                fetch['proxy_username'] = proxy_splited.username
            if proxy_splited.password:
                fetch['proxy_password'] = proxy_splited.password
            if six.PY2:
                for key in ('proxy_host', 'proxy_username', 'proxy_password'):
                    if key in fetch:
                        fetch[key] = fetch[key].encode('utf8')
            fetch['proxy_port'] = proxy_splited.port or 8080

        # etag
        if task_fetch.get('etag', True):
            _t = None
            if isinstance(task_fetch.get('etag'), six.string_types):
                _t = task_fetch.get('etag')
            elif track_ok:
                _t = track_headers.get('etag')
            if _t and 'If-None-Match' not in fetch['headers']:
                fetch['headers']['If-None-Match'] = _t
        # last modifed
        if task_fetch.get('last_modified', task_fetch.get('last_modifed', True)):
            last_modified = task_fetch.get('last_modified', task_fetch.get('last_modifed', True))
            _t = None
            if isinstance(last_modified, six.string_types):
                _t = last_modified
            elif track_ok:
                _t = track_headers.get('last-modified')
            if _t and 'If-Modified-Since' not in fetch['headers']:
                fetch['headers']['If-Modified-Since'] = _t
        # timeout
        if 'timeout' in fetch:
            fetch['request_timeout'] = fetch['timeout']
            del fetch['timeout']
        # data rename to body
        if 'data' in fetch:
            fetch['body'] = fetch['data']
            del fetch['data']

        return fetch

    def http_fetch(self, url, task):
        '''HTTP fetcher'''
        start_time = time.time()
        handle_error = lambda x: self.handle_error('http', url, task, start_time, x)

        # setup request parameters
        fetch = self.pack_tornado_request_parameters(url, task)
        task_fetch = task.get('fetch', {})

        session = cookies.RequestsCookieJar()
        # fix for tornado request obj
        if 'Cookie' in fetch['headers']:
            c = http_cookies.SimpleCookie()
            try:
                c.load(fetch['headers']['Cookie'])
            except AttributeError:
                c.load(utils.utf8(fetch['headers']['Cookie']))
            for key in c:
                session.set(key, c[key])
            del fetch['headers']['Cookie']
        if 'cookies' in fetch:
            session.update(fetch['cookies'])
            del fetch['cookies']

        max_redirects = task_fetch.get('max_redirects', 5)
        # we will handle redirects by hand to capture cookies
        fetch['follow_redirects'] = False

        # making requests
        while True:
            # robots.txt
            if task_fetch.get('robots_txt', False):
                can_fetch = self.can_fetch(fetch['headers']['User-Agent'], fetch['url'])
                if not can_fetch:
                    error = tornado.httpclient.HTTPError(403, 'Disallowed by robots.txt')
                    return handle_error(error)

            try:
                request = tornado.httpclient.HTTPRequest(**fetch)
                # if cookie already in header, get_cookie_header wouldn't work
                old_cookie_header = request.headers.get('Cookie')
                if old_cookie_header:
                    del request.headers['Cookie']
                cookie_header = cookies.get_cookie_header(session, request)
                if cookie_header:
                    request.headers['Cookie'] = cookie_header
                elif old_cookie_header:
                    request.headers['Cookie'] = old_cookie_header
            except Exception as e:
                logger.exception(fetch)
                return handle_error(error)

            try:
                response = self.http_client.fetch(request)
            except tornado.httpclient.HTTPError as e:
                if e.response:
                    response = e.response
                else:
                    return handle_error(error)

            extract_cookies_to_jar(session, response.request, response.headers)
            if (response.code in (301, 302, 303, 307)
                    and response.headers.get('Location')
                    and task_fetch.get('allow_redirects', True)):
                if max_redirects <= 0:
                    error = tornado.httpclient.HTTPError(
                        599, 'Maximum (%d) redirects followed' % task_fetch.get('max_redirects', 5),
                        response)
                    return handle_error(error)
                if response.code in (302, 303):
                    fetch['method'] = 'GET'
                    if 'body' in fetch:
                        del fetch['body']
                # fetch['url'] = quote_chinese(urljoin(fetch['url'], response.headers['Location']))
                fetch['request_timeout'] -= time.time() - start_time
                if fetch['request_timeout'] < 0:
                    fetch['request_timeout'] = 0.1
                max_redirects -= 1
                continue

            result = {}
            result['orig_url'] = url
            result['content'] = response.body or ''
            result['headers'] = dict(response.headers)
            result['status_code'] = response.code
            result['url'] = response.effective_url or url
            result['time'] = time.time() - start_time
            result['cookies'] = session.get_dict()
            result['save'] = task_fetch.get('save')
            if response.error:
                result['error'] = utils.text(response.error)
            if 200 <= response.code < 300:
                print("[%d] %s:%s %s %.2fs" % (response.code,
                            task.get('project'), task.get('taskid'),
                            url, result['time']))
            else:
                print("[%d] %s:%s %s %.2fs" % (response.code,
                               task.get('project'), task.get('taskid'),
                               url, result['time']))

            return result

    def splash_fetch(self, url, task):
        '''Fetch with splash'''
        start_time = time.time()
        handle_error = lambda x: self.handle_error('splash', url, task, start_time, x)

        # check phantomjs proxy is enabled
        if not self.splash_endpoint:
            result = {
                "orig_url": url,
                "content": "splash is not enabled.",
                "headers": {},
                "status_code": 501,
                "url": url,
                "time": time.time() - start_time,
                "cookies": {},
                "save": task.get('fetch', {}).get('save')
            }
            logger.warning("[501] %s:%s %s 0s", task.get('project'), task.get('taskid'), url)
        else:
            # setup request parameters
            fetch = self.pack_tornado_request_parameters(url, task)
            task_fetch = task.get('fetch', {})
            for each in task_fetch:
                if each not in fetch:
                    fetch[each] = task_fetch[each]

            # robots.txt
            if task_fetch.get('robots_txt', False):
                user_agent = fetch['headers']['User-Agent']
                can_fetch = self.can_fetch(user_agent, url)
                if not can_fetch:
                    error = tornado.httpclient.HTTPError(403, 'Disallowed by robots.txt')
                    return handle_error(error)

            request_conf = {
                'follow_redirects': False,
                'headers': {
                    'Content-Type': 'application/json',
                }
            }
            request_conf['connect_timeout'] = fetch.get('connect_timeout', 20)
            request_conf['request_timeout'] = fetch.get('request_timeout', 120) + 1

            session = cookies.RequestsCookieJar()
            if 'Cookie' in fetch['headers']:
                c = http_cookies.SimpleCookie()
                try:
                    c.load(fetch['headers']['Cookie'])
                except AttributeError:
                    c.load(utils.utf8(fetch['headers']['Cookie']))
                for key in c:
                    session.set(key, c[key])
                del fetch['headers']['Cookie']
            if 'cookies' in fetch:
                session.update(fetch['cookies'])
                del fetch['cookies']

            request = tornado.httpclient.HTTPRequest(url=fetch['url'])
            cookie_header = cookies.get_cookie_header(session, request)
            if cookie_header:
                fetch['headers']['Cookie'] = cookie_header

            # making requests
            fetch['lua_source'] = self.splash_lua_source
            fetch['headers'] = dict(fetch['headers'])
            try:
                request = tornado.httpclient.HTTPRequest(
                    url=self.splash_endpoint, method="POST",
                    body=json.dumps(fetch), **request_conf)
            except Exception as e:
                return handle_error(e)

            try:
                response = self.http_client.fetch(request)
            except tornado.httpclient.HTTPError as e:
                if e.response:
                    response = e.response
                else:
                    return handle_error(e)

            if not response.body:
                return handle_error(Exception('no response from phantomjs'))

            result = {}
            try:
                result = json.loads(utils.text(response.body))
                assert 'status_code' in result, result
            except ValueError as e:
                logger.error("result is not json: %r", response.body[:500])
                return handle_error(e)
            except Exception as e:
                if response.error:
                    result['error'] = utils.text(response.error)
                return handle_error(e)

            if result.get('status_code', 200):
                logger.info("[%d] %s:%s %s %.2fs", result['status_code'],
                            task.get('project'), task.get('taskid'), url, result['time'])
            else:
                logger.error("[%d] %s:%s %s, %r %.2fs", result['status_code'],
                             task.get('project'), task.get('taskid'),
                             url, result['content'], result['time'])

        return result

    def phantom_js_fetch(self, url, task):
        '''Fetch with phantomjs proxy'''
        start_time = time.time()
        handle_error = lambda x: self.handle_error('phantomjs', url, task, start_time, x)
        # check phantomjs proxy is enabled
        if not self.phantom_js_proxy:
            result = {
                "orig_url": url,
                "content": "phantomjs is not enabled.",
                "headers": {},
                "status_code": 501,
                "url": url,
                "time": time.time() - start_time,
                "cookies": {},
                "save": task.get('fetch', {}).get('save')
            }
            print("[501] %s:%s %s 0s" % (task.get('project'), task.get('taskid'), url))
        else:
            # setup request parameters
            fetch = self.pack_tornado_request_parameters(url, task)
            task_fetch = task.get('fetch', {})
            for each in task_fetch:
                if each not in fetch:
                    fetch[each] = task_fetch[each]
            # robots.txt
            if task_fetch.get('robots_txt', False):
                user_agent = fetch['headers']['User-Agent']
                can_fetch = self.can_fetch(user_agent, url)
                if not can_fetch:
                    error = tornado.httpclient.HTTPError(403, 'Disallowed by robots.txt')
                    return handle_error(error)
            request_conf = {
                'follow_redirects': False
            }
            request_conf['connect_timeout'] = fetch.get('connect_timeout', 20)
            request_conf['request_timeout'] = fetch.get('request_timeout', 120) + 1
            session = cookies.RequestsCookieJar()
            if 'Cookie' in fetch['headers']:
                c = http_cookies.SimpleCookie()
                try:
                    c.load(fetch['headers']['Cookie'])
                except AttributeError:
                    c.load(utils.utf8(fetch['headers']['Cookie']))
                for key in c:
                    session.set(key, c[key])
                del fetch['headers']['Cookie']
            if 'cookies' in fetch:
                session.update(fetch['cookies'])
                del fetch['cookies']
            request = tornado.httpclient.HTTPRequest(url=fetch['url'])
            cookie_header = cookies.get_cookie_header(session, request)
            if cookie_header:
                fetch['headers']['Cookie'] = cookie_header

            # making requests
            fetch['headers'] = dict(fetch['headers'])
            try:
                request = tornado.httpclient.HTTPRequest(
                    url=self.phantom_js_proxy, method="POST",
                    body=json.dumps(fetch), **request_conf)
            except Exception as e:
                return handle_error(e)
            try:
                response = self.http_client.fetch(request)
            except tornado.httpclient.HTTPError as e:
                if e.response:
                    response = e.response
                else:
                    return handle_error(error)
            if not response.body:
                result = handle_error(Exception('no response from phantomjs: %r' % response))
            try:
                result = json.loads(utils.text(response.body))
                assert 'status_code' in result, result
            except Exception as e:
                if response.error:
                    result['error'] = utils.text(response.error)
                return handle_error(error)
            if result.get('status_code', 200):
                print("[%d] %s:%s %s %.2fs" % (result['status_code'],
                            task.get('project'), task.get('taskid'), url, result['time']))
            else:
                print("[%d] %s:%s %s, %r %.2fs" % (result['status_code'],
                             task.get('project'), task.get('taskid'),
                             url, result['content'], result['time']))
        return result

    def handle_error(cls, type, url, task, start_time, error):
        result = {
            'status_code': getattr(error, 'code', 599),
            'error': str(error),
            'traceback': traceback.format_exc() if sys.exc_info()[0] else None,
            'content': "",
            'time': time.time() - start_time,
            'orig_url': url,
            'url': url,
        }
        print("[%d] %s:%s %s, %r %.2f" %
              (result['status_code'], task.get('project'), task.get('taskid'), url, error, result['time']))
        return result
        
class webfetcher(DalBaseUnit):
    def __init__(self):
        self._start_frame()

    def puIF1_Info(self):
        retInfo={}
        retInfo['accode'] = '111'
        retInfo['desc'] = 'this is description of puIF1'
        retInfo['example'] = '''{
            'parameter1' : 'par1',
            'parameter2' : 'par2'
        }'''
        return retInfo

    def puIF1_Meta(self,dicUser,dicInput):
        retMeta={}
        if 'url' in dicInput:
            dicRet = self._fetch_web(dicInput['url'])
            print('Ret:{}'.format(dicRet))
        else:
            self.logWarn('Input without url part:{}'.format(dicInput))
        return retMeta

    def puIF1_Data(self,dicUser,tupleMeta):
        retData={}
        url = tupleMeta['url']
        fetchRet = self._fetch_web(url)
        retData['content'] = fetchRet
        retData['dtime']='20200503T113753.300'
        retData['value']='15672'
        return retData

    def puIF1_NewData(self):
        return

    def _fetch_web(self,url):
        #todo, add catch for meta and data use
        #real ask interval for same page should be 1 second
        key = dict()
        key['data'] = 'web'
        key['url'] = url
        key['craw_config'] = {'headers': {'Accept-Encoding': 'gzip, deflate'}}
        webF = Fetcher()
        fetchRet = webF.fetch_web(key)
        return fetchRet

    def test(self):
        dicInfo = self.puIF1_Info()
        print('IF1 info:{}',dicInfo)

        dicUser={}
        dicUser['name']='hellodal'
        dicUser['accountStauts']='normal'
        dicUser['uidNumber']=500
        dicUser['gidNumber']=200
        dicUser['description']='this is a sample user'
        dicUser['listGPID']=['201','202']
        dicInput={}
        dicInput['url'] = 'http://www.baidu.com'
        dicMeta = self.puIF1_Meta(dicUser,dicInput)
        print('IF1 meta:{}',dicMeta)

        dicData = self.puIF1_Data(dicUser,dicMeta)
        print('IF1 data:{}',dicData)

        # time.sleep(20)   
        self.quit()

if __name__ == '__main__':
    pcu = webfetcher() 
    pcu.test()
