# -*- coding: utf-8 -*- 

from datetime import  *  
from enum import IntEnum
from iqsopenapi.models.Order import *
from iqsopenapi.models.Contract import *

class Trade(object):
    """成交信息"""

    def __init__(self):
        """成交信息"""

        """订单ID"""
        self.trade_id = ""

        """订单ID"""
        self.order_id = ""

        """策略编号"""
        self.strategy_id = ""

        """账户编号"""
        self.account_id = ""

        """股票代码或合约代码"""
        self.symbol = ""

        """交易所"""
        self.exchange = Exchange.UnKnow

        """委托方向"""
        self.side = OrderSide.Buy

        """委托价格"""
        self.price = 0.0

        """开仓还是平仓 (期货中使用) 非期货为None"""
        self.offset = Offset.UnKnow

        """委托数量"""
        self.quantity = 0

        """成交时间"""
        self.filled_time = datetime.now()