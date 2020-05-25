# -*- coding: utf-8 -*-
class IMarketApi(object):
    """行情接口"""

    def __init__(self,event_bus):
        """构造函数"""
        pass

    def Init(self,strategyID):
        """初始化"""
        pass

    def GetSubscibes(self):
        """获取订阅列表"""
        pass

    def Subscribe(self,*subInfos):
        """行情订阅"""
        pass

    def Unsubscribe(self,*subInfos):
        """取消订阅"""
        pass

    def GetHisBar(self, symbol, exchange, barType, startTime, endTime):
        """获取历史K线数据"""
        pass

    def GetLastBar(self, symbol, exchange, barType, count):
        """获取历史K线数据"""
        pass

    def GetHisTick(self, symbol, exchange, startTime, endTime):
        """获取历史TICK数据"""
        pass

    def GetLastTick(self, symbol, exchange, count):
        """获取历史TICK数据"""
        pass
