# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
from jdu.core import exceptions
from jdu.api.base import JDUWebAPI


class ReceiveCode(JDUWebAPI):

    def get_code(self, material_id=None, coupon_link=None, material_type=1, plan_id=None, is_pin_gou=0,
                 promotion_type=15, receive_type='cps', ware_url=None, is_smart_graphics=None):

        url = 'https://union.jd.com/api/receivecode/getCode'

        ext_headers = {
            'referer': 'https://union.jd.com/proManager/index?pageNo=1',
        }

        data = {
            'couponLink': coupon_link,
            'materialId': material_id,
            'materialType': material_type,
            'isPinGou': is_pin_gou,
            'planId': plan_id,
            'promotionType': promotion_type,
            'receiveType': receive_type,
            'wareUrl': ware_url,
            'isSmartGraphics': is_smart_graphics,
            # 'requestId': 's_45f85c81ee1a4dadb1678b5e56317737'
        }

        package = {
            'data': data
        }

        def decode_result(result, response, client=None, **kwargs):
            if result.get('code') != 200:
                raise exceptions.JDUClientException(
                    result.get('code'),
                    result.get('message'),
                    client=client,
                    request=response.request,
                    response=response
                )
            result = result.get('data', {})
            return result

        return self.post(url, package, ext_headers=ext_headers, result_processor=decode_result)
