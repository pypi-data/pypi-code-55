# -*- coding: utf-8 -*-
class IBasicDataApi(object):
    """基础数据接口"""

    def __init__(self):
        """构造函数"""
        pass

    def GetContract(self, symbol, exchange):
        """获取合约信息"""
        pass

    def GetMainContract(self, variety):
        """获取主力合约信息（期货）"""
        pass

    def GetOpenTimes(self,begin,end):
        """获取开盘时间"""
        pass

