# -*- coding: utf-8 -*- 

from datetime import *
from iqsopenapi.models.Contract import *

class BarData(object):
    """历史数据模型"""

    def __init__(self):

        """合约或股票代码名称"""
        self.symbol = ""

        """交易所"""
        self.exchange = Exchange.UnKnow

        """周期类型以秒计算"""
        self.bar_type = 0

        """时间"""
        self.local_time = datetime.now()

        """昨收"""
        self.pre_close = 0.0

        """开盘价"""
        self.open = 0.0

        """最高价"""
        self.high = 0.0

        """最低价"""
        self.low = 0.0

        """收盘价"""
        self.close = 0.0

        """成交量"""
        self.volume = 0

        """成交额"""
        self.turnover = 0.0      

        """持仓量"""
        self.open_interest = 0

        """结算价"""
        self.settlement = 0.0  


        

        

        

        

        

        


