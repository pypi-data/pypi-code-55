# -*- coding:utf-8 -*-
__author__ = 'Dragon Sun'
__date__ = '2020-01-31 19:30:13'

from dsQtCommon.fields.stock.fields import *
from dsQtCommon.fields.common.fields import *


class DBBaseBar(DBBaseModel):
    """ K线数据基类(供派生) """

    code = StockCodeField(index=True)  # 股票编码
    slot = BarSlotField(index=True)  # 时间槽
    open = StockPriceField()  # 开盘价
    high = StockPriceField()  # 最高价
    low = StockPriceField()  # 最低价
    close = StockPriceField()  # 收盘价
    volume = StockVolumeField()  # 成交量(股)
    amount = StockAmountField()  # 成交额(元)
    change = StockRatioField()  # 涨幅%
    amplitude = StockRatioField()  # 振幅%
    turn = StockRatioField()  # 换手率%
    kind = BarKindField()  # K线类型
    real_kind = BarKindField()  # K线真实类型
    fq = StockFQKindField(index=True)  # 复权方式

    class Meta:
        primary_key = CompositeKey('code', 'slot', 'fq')
        indexes = (
            (('code', 'slot', 'fq'), True),
        )
