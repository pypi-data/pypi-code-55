from scrapy.http import Response


class ScrapingBeeResponse(Response):

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)
