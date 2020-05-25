# -*- coding: utf-8 -*-
class ITradeApi(object):
    """交易接口"""

    def __init__(self,event_bus):
        """构造函数"""
        pass

    def Init(self):
        """初始化"""
        pass

    def SendOrder(self,symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        pass

    def CancelOrder(self,order):
        """撤单"""
        pass

    def GetAccount(self):
        """获取账户信息"""
        pass

    def GetOrder(self,orderId):
        """获取指定id的委托"""
        pass

    def GetOpenOrders(self):
        """获取打开的订单"""
        pass

    def GetOrders(self):
        """获取当日委托"""
        pass

    def GetPositions(self):
        """获取持仓"""
        pass

    def GetTrades(self):
        """获取当日成交"""
        pass