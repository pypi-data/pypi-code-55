# -*- coding: utf-8 -*- 

from enum import IntEnum
from iqsopenapi.models.Contract import *

class Position(object):
    """持仓信息"""

    def __init__(self):
        
        
        """策略编号"""
        self.strategy_id = ""

        """账户编号"""
        self.account_id = ""

        """股票代码或合约代码"""
        self.symbol = ""

        """交易所"""
        self.exchange = Exchange.UnKnow

        """最新行情价"""
        self.last_px = 0.0

        """持仓数量"""
        self.quantity = 0

        """冻结数量"""
        self.frozen = 0

        """持仓成本"""
        self.cost = 0.0

        """持仓方向"""
        self.side = PosSide.Net

        """保证金"""
        self.margin = 0.0

        """市值"""
        self.value = 0.0

        """浮动盈亏"""
        self.profit = 0.0

        """今仓"""
        self.today_qty = 0.0

        """今仓可用"""
        self.today_avl = 0.0

class PosSide(IntEnum):
        """持仓方向"""

        """净持仓"""
        Net = 0
        """多仓"""
        Long = 1
        """空仓"""
        Short = 2