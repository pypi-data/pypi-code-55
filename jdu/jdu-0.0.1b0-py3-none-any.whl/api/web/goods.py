# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import uuid
from jdu.core import exceptions
from jdu.api.base import JDUWebAPI


class Goods(JDUWebAPI):
    def search(self, key=None, page_no=1, page_size=60, category_id=None, cat2_id=None, cat3_id=None, bonus_ids=None,
               delivery_type=0, from_commission_ratio=None, to_commission_ratio=None, from_price=None, to_price=None,
               has_coupon=0, is_hot=None, is_pin_gou=0, is_zy=0, is_care=0, lock=0, orientation_flag=0, sort=None,
               sort_name=None, search_type='st1', keyword_type='kt1'):

        url = 'https://union.jd.com/api/goods/search'

        ext_headers = {
            'referer': 'https://union.jd.com/proManager/index',
        }

        search_uuid = str(uuid.uuid4()).replace('-', '')

        search_data = {
            'key': key,
            'bonusIds': bonus_ids,
            'categoryId': category_id,
            'cat2Id': cat2_id,
            'cat3Id': cat3_id,
            'deliveryType': delivery_type,
            'fromCommissionRatio': from_commission_ratio,
            'toCommissionRatio': to_commission_ratio,
            'fromPrice': from_price,
            'toPrice': to_price,
            'hasCoupon': has_coupon,
            'isHot': is_hot,
            'isPinGou': is_pin_gou,
            'isZY': is_zy,
            'isCare': is_care,
            'lock': lock,
            'orientationFlag': orientation_flag,
            'sort': sort,
            'sortName': sort_name,
            'searchType': search_type,
            'keywordType': keyword_type,
        }

        package = {
            'pageNo': page_no,
            'pageSize': page_size,
            'searchUUID': search_uuid,
            'data': search_data
        }


        return self.post(url, package, ext_headers=ext_headers)
