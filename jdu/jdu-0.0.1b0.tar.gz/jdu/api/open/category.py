# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
from jdu.api.base import JDUOpenAPI


class Category(JDUOpenAPI):

    def goods_get(self, parent_id, grade):
        """
        商品类目查询接口
        文档: https://union.jd.com/openplatform/api/10434

        :param parent_id: 父类目id(一级父类目为0)
        :param grade: 类目级别(类目级别 0，1，2 代表一、二、三级类目)
        :return:
        """
        api_method = 'jd.union.open.category.goods.get'

        req = {
            'parentId': parent_id,
            'grade': grade
        }

        params = {
            'req': req
        }

        return self.get(api_method, params)
