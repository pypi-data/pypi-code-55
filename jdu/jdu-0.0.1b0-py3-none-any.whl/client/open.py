# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)

from jdu.client.base import BaseClient
from jdu.api.open.category import Category
from jdu.api.open.goods import Goods
from jdu.api.open.order import Order
from jdu.api.open.promotion import Promotion

# todo child_union_id

class JDUOpenApiClient(BaseClient):
    goods = Goods()
    category = Category()
    promotion = Promotion()
    order = Order()

    def __init__(self, app_key, app_secret, site_id=None, sub_union_id=None, version='1.0', timeout=None, auto_retry=True, *args, **kwargs):
        super(JDUOpenApiClient, self).__init__(timeout, auto_retry, *args, **kwargs)
        self.app_key = app_key
        self.app_secret = app_secret
        self.version = version
        self.site_id = site_id
        self.sub_union_id = sub_union_id

    def _request(self, method, uri, **kwargs):

        return super(JDUOpenApiClient, self)._request(method, uri, **kwargs)


