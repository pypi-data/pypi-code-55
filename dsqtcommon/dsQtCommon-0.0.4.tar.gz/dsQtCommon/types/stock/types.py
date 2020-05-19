# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-05-18 15:40:38'

"""
    stock.types
"""

from enum import unique, Enum


# 交易所
@unique
class StockExchange(Enum):
    sh = '上海'
    sz = '深圳'


# 股票市场
@unique
class StockMarket(Enum):
    sh_index = '上指'  # 上指
    sh_stock = '上交所主板'  # 上交所主板
    sh_sti = '上交所科创板'  # 上交所科创板(science and technology innovation board)
    sz_index = '深指'  # 深指
    sz_stock = '深交所主板'  # 深交所主板
    sz_sme = '深交所中小板'  # 深交所中小板(small and medium enterprise board)
    sz_gem = '深交所创业板'  # 深交所创业板(growth enterprise market)


# 股票品质
@unique
class StockQuality(Enum):
    normal = 'normal'  # 正常
    st = 'ST'  # ST
    st_plus = '*ST'  # *ST


# 股票K线周期
@unique
class StockBarFreq(Enum):
    min5 = '5'
    min15 = '15'
    min30 = '30'
    min60 = '60'
    day = 'd'
    week = 'w'
    month = 'm'


# 股票K线复权方式
@unique
class StockBarFQ(Enum):
    before = 2  # '前复权'
    none = 3  # '不复权'
    after = 1  # '后复权'
