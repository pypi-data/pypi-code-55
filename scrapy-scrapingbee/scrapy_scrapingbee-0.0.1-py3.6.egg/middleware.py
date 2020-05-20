import copy

from scrapy import Request

from .request import ScrapingBeeRequest


class ScrapingBeeMiddleware:
    scrapingbee_api_url = 'https://app.scrapingbee.com/api/v1/'

    def __init__(self, api_key):
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        api_key = crawler.settings.get('SCRAPINGBEE_API_KEY')
        return cls(api_key=api_key)

    def _process_url(self, url, params):
        qs_params = {
            'api_key': self.api_key,
        }
        qs_params.update(params)
        
        qs = '&'.join(f'{k}={v}' for k, v in qs_params.items())
        return f'{self.scrapingbee_api_url}?{qs}'

    def process_request(self, request, spider):
        print(request.meta)
        raise
        if not isinstance(request, ScrapingBeeRequest):
            return
        
        if 'processed' in request.meta['scrapingbee']:
            return

        meta = copy.deepcopy(request.meta)
        meta['scrapingbee']['processed'] = True

        url = self._process_url(
            request.url, meta['scrapingbee']['params'])
        new_request = request.replace(url=url, meta=meta)
        
        return new_request

    def process_response(self, request, response, spider):
        if not isinstance(request, ScrapingBeeRequest):
            return response

        # Modify response url to original request url
        response = response.replace(url=request.url)

        return response
