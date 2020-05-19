# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-05-18 12:57:56'

"""
    stock.fields
"""

from dsPyLib.peewee.db_base_model import *


# 股票代码字段(例如：sh.600218)
class StockCodeField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_length=9, *args, **kwargs)


# 股票数字编码字段(例如：600218)
class StockNumberField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_length=6, *args, **kwargs)


# 股票交易所名称字段
class StockExchangeNameField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_length=8, *args, **kwargs)


# 股票板块(市场)名称字段
class StockMarketNameField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_length=6, *args, **kwargs)


# 股票名称字段
class StockNameField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_length=32, *args, **kwargs)


# 股票品质字段
class StockQualityNameField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_length=6, *args, **kwargs)


# 股票价格字段
class StockPriceField(DecimalField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_digits=8, decimal_places=2, auto_round=True, *args, **kwargs)


# 股票成交量字段(股)
class StockVolumeField(BigIntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# 股票成交额字段(元)
class StockAmountField(DecimalField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_digits=16, decimal_places=2, auto_round=True, *args, **kwargs)


# 股票百分比字段(单位%)
class StockRatioField(DecimalField):
    def __init__(self, *args, **kwargs):
        super().__init__(max_digits=6, decimal_places=2, auto_round=True, *args, **kwargs)


# 股票复权方式字段(1 - 后复权; 2 - 前复权; 3 - 不复权)
class StockFQKindField(SmallIntegerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
