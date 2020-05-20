import requests
from abc import ABC, abstractmethod
from .user_agents import user_agents_list
import copy
import time
from .proxy_helper import ProxyHelper, BadProxyError, ProxySettings


class Downloader(ABC):

    def __init__(self, logger, proxy_settings=ProxySettings, use_session=False, attempts=20,
                 use_user_agents=True) -> None:
        self.logger = logger
        self.attempts = attempts
        self.user_agents_list = user_agents_list
        self.use_session = use_session
        self.use_user_agents = use_user_agents

        self.initialize_request_maker()
        self.proxy_auth = {}
        self.proxy_settings = proxy_settings
        self.proxy_helper = ProxyHelper(self.logger, self.proxy_settings)

    def get_proxies(self, proxy):
        """
        Creating proxy object from simple proxy string
        :param proxy: proxy string with {ip}:{port} pattern
        :type proxy: str
        :return: proxy object
        :rtype: dict
        """
        # get login and password if proxy required logining
        login = self.proxy_auth.get(proxy, {}).get('login', '')
        password = self.proxy_auth.get(proxy, {}).get('password', '')
        proxy_string = '{}' + f'://{login}:{password}@{proxy}'
        proxies = {'https': proxy_string.format('https'),
                   'http': proxy_string.format('http')}
        return proxies

    def create_request(self, method, url, params={}, cookies=None, data={}, headers={}, timeout=60, files=None):
        # Decorator must use instant function because we must change instant proxy dataframe only
        @self.proxy_helper.exception_decorator
        def request_to_page(proxy, **kwargs):
            """
            Request wrapper
            :param proxy: proxy string with {ip}:{port} pattern
            :type proxy: str
            :param kwargs: request params
            :return: response text
            :rtype: str
            """
            proxies = self.get_proxies(proxy) if proxy else {}
            start_time = time.time()
            response = self.request_maker.request(proxies=proxies, stream=True, **kwargs)
            full_content = b''
            for content in response.iter_content(1024):
                if time.time() - start_time > 30:
                    # if request time longer than 30 sec must stop request
                    raise BadProxyError
                full_content += content
            response._content = full_content

            return response

        headers = copy.deepcopy(headers)
        attempts = self.attempts
        while attempts > 0:
            if self.use_user_agents:
                random_agent = self.proxy_helper.get_user_agent()
                headers.update({'user-agent': random_agent})

            attempts -= 1
            # try without proxies last time
            raw_proxy = self.proxy_helper.get_proxy() if self.proxy_settings.use_proxy and attempts != 1 else None
            try:
                request_response = request_to_page(proxy=raw_proxy,
                                                   method=method,
                                                   url=url,
                                                   params=params,
                                                   cookies=cookies,
                                                   data=data,
                                                   headers=headers,
                                                   timeout=timeout,
                                                   files=files)

                return request_response
            except Exception as e:
                if isinstance(e, BadProxyError):
                    attempts += 1
                self.logger.write(10,
                                  'received {} exception on request on {} try on {} link'.format(e,
                                                                                                 self.attempts - attempts,
                                                                                                 url))

    def initialize_request_maker(self) -> None:
        """Session initializing.

        @:param self:
        @:type self: Downloader

        Enables session for requests if self.use_session else all requests without session.

        @:returns: None
        @:rtype: NoneType
        """

        if self.use_session:
            self.request_maker = requests.Session()
            # raise max pool size for use bigger thread pool size
            a = requests.adapters.HTTPAdapter(pool_maxsize=9999)
            self.request_maker.mount('https://', a)
        else:
            self.request_maker = requests

    def get(self, url, params={}, headers={}, cookies={}, timeout=60):
        """Makes 'GET' request with args by using create_request function.

        @:param self:
        @:param url: URL
        @:param params: params for 'GET' request
        @:param headers: request headers
        @:param cookies: request cookies
        @:param timeout: request timeout
        @:param return_response: enable to return response object
        @:param return_response_text: enable to return analog of response.text
        @:type self: Downloader
        @:type url: str
        @:type params: dict
        @:type headers: dict
        @:type cookies: dict
        @:type timeout: int

        Calls create_request function with args for 'GET' request.

        @:returns: tuple of response and response content
        @:rtype: tuple
        """
        return self.create_request(method='GET',
                                   url=url,
                                   params=params,
                                   cookies=cookies,
                                   headers=headers,
                                   timeout=timeout,
                                   )

    def post(self, url, data={}, headers={}, cookies={}, timeout=60):
        """Makes 'POST' request with args by using create_request function.

        @:param self:
        @:param url: URL
        @:param data: data for 'POST' request
        @:param headers: request headers
        @:param cookies: request cookies
        @:param timeout: request timeout
        @:param return_response: enable to return response object
        @:param return_response_text: enable to return analog of response.text
        @:type self: Downloader
        @:type url: str
        @:type data: dict
        @:type headers: dict
        @:type cookies: dict
        @:type timeout: int


        Calls create_request function with args for 'POST' request.

        @:returns: tuple of response and response content
        @:rtype: tuple
        """
        return self.create_request(method='POST',
                                   url=url,
                                   cookies=cookies,
                                   data=data,
                                   headers=headers,
                                   timeout=timeout,
                                   )
