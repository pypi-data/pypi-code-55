# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import random

from scrapy import signals
from scrapy.exceptions import NotConfigured


class OsScrapyRandomProxySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class OsScrapyRandomProxyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    def __init__(self, crawler):
        self.crawler = crawler
        self.proxy_list = []
        try:
            self.load()
        except Exception as e:
            raise NotConfigured(f'load fail {e}')

    @classmethod
    def from_crawler(cls, crawler):
        if crawler.settings.get('PROXIES', None) is None:
            raise NotConfigured('not set PROXIES')
        return cls(crawler)

    def load(self):
        proxies = self.crawler.settings.get('PROXIES')

        # PROXIES is a list
        if isinstance(proxies, list):
            proxy_list = [proxy.strip() for proxy in proxies if len(proxy.strip()) > 0]
            if len(proxies) <= 0:
                raise Exception('no available proxy')
            self.proxy_list = proxy_list
            return

        # PROXIES is a str, maybe a single proxy or a file path
        elif isinstance(proxies, str):
            proxies = proxies.strip()
            if os.path.isfile(proxies):
                with open(proxies, 'r') as f:
                    proxy_list = [proxy.strip() for proxy in f.readlines() if len(proxy.strip()) > 0]
                    if len(proxy_list) <= 0:
                        raise Exception(f'no availabel proxy in file {proxies}')
                    self.proxy_list = proxy_list
            else:
                if len(proxies) <= 0:
                    raise Exception('empty string')
                self.proxy_list = [proxies]
            return
        raise Exception(f'invalid PROXIES {proxies}')

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list)
        request.meta['proxy'] = proxy

