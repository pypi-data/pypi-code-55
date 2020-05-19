from scrapy.exceptions import DropItem
import requests


class RequestPipeline(object):

    def __init__(self, request_addr, request_try_count, request_timeout, request_success_status_code, request_verify):
        self.request_addr = request_addr
        self.request_try_count = request_try_count or 5
        self.request_timeout = request_timeout or 5
        self.request_success_status_code = request_success_status_code or 200
        self.request_verify = request_verify or False

    def process_item(self, item, spider):

        if self.request_addr == '':
            spider.logger.info(f'spider {spider.name} no REQUEST_ADDR setting')
            return item

        unique_id = item['unique_id']
        if not unique_id:
            raise DropItem('unique_id is None')

        data = item.deepcopy().to_dict()
        for retry_count in range(self.request_try_count):
            response = requests.post(self.request_addr, json=data, timeout=self.request_timeout,
                                     verify=self.request_verify)
            if int(response.status_code) == self.request_success_status_code:
                spider.logger.info(f'req addr: {self.request_addr}  {unique_id} request success')
                return item

        spider.logger.info(f'req addr: {self.request_addr} {unique_id} request fail, {response.status_code} {data}')

        return item

    def open_spider(self, spider):
        spider.logger.info(f'spider {spider.name} request pipeline open')
        pass

    def close_spider(self, spider):
        spider.logger.info(f'spider {spider.name} request pipeline closed')
        pass

    @classmethod
    def from_crawler(cls, crawler):
        if crawler.spider is None:
            return
        request_addr = crawler.spider.settings.get('REQUEST_ADDR')
        request_try_count = crawler.spider.settings.get('REQUEST_TRY_COUNT')
        request_timeout = crawler.spider.settings.get('REQUEST_TIMEOUT')
        request_success_status_code = crawler.spider.settings.get('REQUEST_SUCCESS_STATUS_CODE')
        request_verify = crawler.spider.settings.get('REQUEST_VERIFY')
        return cls(
            request_addr,
            request_try_count,
            request_timeout,
            request_success_status_code,
            request_verify
        )
