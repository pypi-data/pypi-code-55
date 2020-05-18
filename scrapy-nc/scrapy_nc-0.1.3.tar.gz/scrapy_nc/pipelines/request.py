from scrapy.exceptions import DropItem
import requests


class RequestPipeline(object):

    def process_item(self, item, spider):

        if hasattr(spider, 'request_addr') == False:
            spider.logger.info(f'spider {spider.name} no request_addr attr')
            return item

        request_try_count = 5
        if hasattr(spider, 'request_try_count'):
            request_try_count = int(spider.request_try_count)

        request_timeout = 5
        if hasattr(spider, 'request_timeout'):
            request_timeout = int(spider.request_timeout)

        request_success_status_code = 200
        if hasattr(spider, 'request_success_status_code'):
            request_success_status_code = int(spider.request_success_status_code)

        req_url = spider.request_addr

        unique_id = item['unique_id']
        if not unique_id:
            raise DropItem('unique_id is None')

        data = item.deepcopy().to_dict()
        for retry_count in range(request_try_count):
            response = requests.post(req_url, json=data, timeout=request_timeout)
            if int(response.status_code) == request_success_status_code:
                spider.logger.info(f'{unique_id} request success')
                return item

        spider.logger.info(f'{unique_id} request fail, {response.status_code} {data}')

        return item

    def open_spider(self, spider):
        spider.logger.info(f'spider {spider.name} request pipeline open')
        pass

    def close_spider(self, spider):
        spider.logger.info(f'spider {spider.name} request pipeline closed')
        pass
