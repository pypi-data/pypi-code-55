# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-30 15:37:34'

from dsQtCommon.fields.stock.fields import *


class DBStockMeta(DBBaseModel):
    """ 股票标的物信息 """

    code = StockCodeField(primary_key=True)  # 股票编码
    number = StockNumberField(index=True)  # 股票6位数字代码
    exchange = StockExchangeNameField()  # 交易所, StockExchange
    market = StockMarketNameField()  # 股票市场, StockMarket
    name = StockNameField()  # 股票名称(不带ST和*ST)
    full_name = StockNameField()  # 股票全称(带ST和*ST)
    quality = StockQualityNameField()  # 股票品质, StockQuality

    class Meta:
        table_name = 'metas'
        indexed = (
            ('code', True)
        )
