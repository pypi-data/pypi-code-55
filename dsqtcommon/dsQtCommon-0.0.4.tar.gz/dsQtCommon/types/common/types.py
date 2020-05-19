# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-05-18 19:45:01'

from enum import unique, Enum


# K线类型
@unique
class BarKind(Enum):
    negative = -1  # 阴线
    cross = 0  # 十字星
    positive = 1  # 阳线
