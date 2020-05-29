# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
from jdu.api.base import JDUOpenAPI


class Promotion(JDUOpenAPI):

    def common_get(self, material_id, site_id=None, position_id=None, sub_union_id=None,
                   ext1=None, pid=None, coupon_url=None,
                   gift_coupon_key=None):
        """
        网站/APP获取推广链接接口
        文档: https://union.jd.com/openplatform/api/10421

        :param material_id: 推广物料 eg: https://item.jd.com/23484023378.html
        :param site_id: 站点ID是指在联盟后台的推广管理中的网站Id、APPID（1、通用转链接口禁止使用社交媒体id入参；2、订单来源，即投放链接的网址或应用必须与传入的网站ID/AppID备案一致，否则订单会判“无效-来源与备案网址不符”）
        :param position_id: 推广位id
        :param sub_union_id: 子联盟ID（需申请，申请方法请见https://union.jd.com/helpcenter/13246-13247-46301），该字段为自定义参数，建议传入字母数字和下划线的格式
        :param ext1: 系统扩展参数，无需传入
        :param pid: 联盟子站长身份标识，格式：子站长ID_子站长网站ID_子站长推广位ID eg: 618_618_6018
        :param coupon_url: 优惠券领取链接，在使用优惠券、商品二合一功能时入参，且materialId须为商品详情页链接 eg: http://coupon.jd.com/ilink/get/get_coupon.action?XXXXXXX
        :param gift_coupon_key: 礼金批次号 eg: xxx_coupon_key
        :return:
        """

        api_method = 'jd.union.open.promotion.common.get'

        if not site_id:
            site_id = self._client.site_id

        if not sub_union_id:
            sub_union_id = self._client.sub_union_id

        promotion_code_req = {
            'materialId': material_id,
            'siteId': site_id,
            'positionId': position_id,
            'subUnionId': sub_union_id,
            'ext1': ext1,
            'pid': pid,
            'couponUrl': coupon_url,
            'giftCouponKey': gift_coupon_key,
        }

        params = {
            'promotionCodeReq': promotion_code_req
        }

        return self.get(api_method, params)
