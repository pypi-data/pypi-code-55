# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-05-18 16:14:26'

"""
    common.fields
"""

from dsPyLib.peewee.db_base_model import *


# K线时间槽字段
class BarSlotField(DateTimeField):
    def __init__(self, *args, **kwargs):
        super().__init__(formats='%Y-%m-%d %H:%M', *args, **kwargs)


# K线类型字段(-1 - 阴线; 0 - 十字星; 1 - 阳线)
class BarKindField(SmallIntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
