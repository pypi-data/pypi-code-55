# -*- coding: utf-8 -*- 

from datetime import  *  
from enum import IntEnum
from iqsopenapi.models.Order import *
from iqsopenapi.models.Contract import *

class Order(object):
    """委托请求"""

    def __init__(self):
        """订单ID"""

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

        """委托时间"""
        self.order_time = datetime.now()

        """委托类型"""
        self.order_type = OrderType.LMT

        """委托状态"""
        self.status = OrderStatus.UnKnow

        """成交数量"""
        self.filled = 0

        """备注，失败时包含失败信息"""
        self.note = ""

    def isopen(self):
        """是否打开的订单"""
        return self.status != OrderStatus.Cancelled and self.status != OrderStatus.Filled and self.status != OrderStatus.Rejected;
     
class OrderType(IntEnum):
        """委托类型"""

        """限价"""
        LMT = 0
        """市价"""
        MKT = 1

class OrderStatus(IntEnum):
        """ 未知""" 
        UnKnow = -1
        """ 未发（下单指令还未发送到下游）"""
        NotSent = 0
        """ 1 已发（下单指令已发送给下游）"""
        Sended = 1
        """ 2 已报（下单指令已报给交易所）"""
        Accepted = 2
        """ 部分成交 """
        PartiallyFilled = 3
        """ 4 已撤（可能已经部分成交，要看看filled字段）"""
        Cancelled = 4
        """ 5 全部成交 """
        Filled = 5
        """ 6 已拒绝 """
        Rejected = 6
        """ 7 撤单请求已发送，但不确定当前状态 """
        PendingCancel = 7

class OrderSide(IntEnum):
        """买卖方向"""

        """买入"""
        Buy = ord('B')
        """卖出"""
        Sell = ord('S')

class Offset(IntEnum):
        """未知"""
        UnKnow = 0
        """开仓""" 
        Open = 1
        """平仓 """ 
        Close = 2
        """ 平今 """
        CloseToday = 3
        """ 平昨 """
        CloseYesterday = 4