# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
from jdu.core.exceptions import ParamTypeError
from jdu.api.base import JDUOpenAPI


class Goods(JDUOpenAPI):

    def jingfen_query(self, elite_id, page_index=1, page_size=20, sort_name=None, sort='desc', pid=None,
                      fields=None):
        """
        京粉精选商品查询接口
        文档: https://union.jd.com/openplatform/api/10417
        :param elite_id: 频道id：1-好券商品,2-超级大卖场,10-9.9专区,22-热销爆品,23-为你推荐,24-数码家电,25-超市,26-母婴玩具,27-家具日用,28-美妆穿搭,29-医药保健,30-图书文具,31-今日必推,32-品牌好货,33-秒杀商品,34-拼购商品,109-新品首发,110-自营,125-首购商品,129-高佣榜单,130-视频商品
        :param page_index: 页码
        :param page_size: 每页数量，默认20，上限50
        :param sort_name: 排序字段(price：单价, commissionShare：佣金比例, commission：佣金， inOrderCount30DaysSku：sku维度30天引单量，comments：评论数，goodComments：好评数)
        :param sort: asc,desc升降序,默认降序
        :param pid: 联盟id_应用id_推广位id，三段式 eg: 618_618_618
        :param fields: 支持出参数据筛选，逗号','分隔，目前可用：videoInfo
        :return:
        """

        api_method = 'jd.union.open.goods.jingfen.query'

        goods_req = {
            'eliteId': elite_id,
            'pageIndex': page_index,
            'pageSize': page_size,
            'sortName': sort_name,
            'sort': sort,
            'pid': pid,
            'fields': fields,
        }

        params = {
            'goodsReq': goods_req
        }

        return self.get(api_method, params)

    def query(self, cid1=None, cid2=None, cid3=None, page_index=1, page_size=20, sku_ids=None, keyword=None,
              price_from=None, price_to=None, commission_share_start=None, commission_share_end=None, owner=None,
              sort_name=None, sort='desc', is_coupon=None, is_pg=None, pingou_price_start=None, pingou_price_end=None,
              is_hot=None, brand_code=None, shop_id=None, has_content=None, has_best_coupon=None, pid=None, fields=None,
              forbid_types=None, jx_flags=None, shop_level_from=None):
        """
        关键词商品查询接口【申请】
        文档: https://union.jd.com/openplatform/api/10420
        :param cid1:
        :param cid2:
        :param cid3:
        :param page_index:
        :param page_size:
        :param sku_ids:
        :param keyword:
        :param price_from:
        :param price_to:
        :param commission_share_start:
        :param commission_share_end:
        :param owner:
        :param sort_name:
        :param sort:
        :param is_coupon:
        :param is_pg:
        :param pingou_price_start:
        :param pingou_price_end:
        :param is_hot:
        :param brand_code:
        :param shop_id:
        :param has_content:
        :param has_best_coupon:
        :param pid:
        :param fields:
        :param forbid_types:
        :param jx_flags:
        :param shop_level_from:
        :return:
        """

        api_method = 'jd.union.open.goods.query'

        if not sku_ids:
            sku_ids = []

        if not jx_flags:
            jx_flags = []

        if not isinstance(sku_ids, (list, tuple)):
            raise ParamTypeError('sku_ids', 'list')

        if not isinstance(jx_flags, (list, tuple)):
            raise ParamTypeError('jx_flags', 'list')

        goods_req_dto = {
            'cid1': cid1,
            'cid2': cid2,
            'cid3': cid3,
            'pageIndex': page_index,
            'pageSize': page_size,
            'skuIds': sku_ids,
            'keyword': keyword,
            'pricefrom': price_from,
            'priceto': price_to,
            'commissionShareStart': commission_share_start,
            'commissionShareEnd': commission_share_end,
            'owner': owner,
            'sortName': sort_name,
            'sort': sort,
            'isCoupon': is_coupon,
            'isPG': is_pg,
            'pingouPriceStart': pingou_price_start,
            'pingouPriceEnd': pingou_price_end,
            'isHot': is_hot,
            'brandCode': brand_code,
            'shopId': shop_id,
            'hasContent': has_content,
            'hasBestCoupon': has_best_coupon,
            'pid': pid,
            'fields': fields,
            'forbidTypes': forbid_types,
            'jxFlags': jx_flags,
            'shopLevelFrom': shop_level_from,

        }

        params = {
            'goodsReqDTO': goods_req_dto
        }

        return self.get(api_method, params)

    def promotiongoodsinfo_query(self, sku_ids):
        """
        根据skuid查询商品信息接口
        文档: https://union.jd.com/openplatform/api/10422

        :param sku_ids: 京东skuID串，逗号分割，最多100个，开发示例如param_json={'skuIds':'5225346,7275691'}（非常重要 请大家关注：如果输入的sk串中某个skuID的商品不在推广中[就是没有佣金]，返回结果中不会包含这个商品的信息）
        :return:
        """
        api_method = 'jd.union.open.goods.promotiongoodsinfo.query'

        params = {
            'skuIds': sku_ids
        }

        return self.get(api_method, params)

