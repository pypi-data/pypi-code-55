# -*- coding: utf-8 -*- 

from datetime import *
from iqsopenapi.models.Contract import *

class TickData(object):
    """实时数据模型"""

    def __init__(self):

        """股票代码或合约名称"""
        self.symbol = ""

        """交易所"""
        self.exchange = Exchange.UnKnow

        """时间"""
        self.local_time = datetime.now()

        """最新成交价"""
        self.last = 0.0

        """成交量"""
        self.volume = 0

        """持仓量"""
        self.open_interest = 0

        """开盘价"""
        self.open = 0.0

        """最高价"""
        self.high = 0.0

        """最低价"""
        self.low = 0.0

        """总成交额"""
        self.turnover = 0.0

        """结算价"""
        self.settlement = 0.0

        """跌停价"""
        self.lower_limit = 0.0

        """涨停价"""
        self.upper_limit = 0.0

        """昨收"""
        self.pre_close = 0.0

        """买N档"""
        self.bids = []

        """卖N档"""
        self.asks = []

class LevelUnit(object):
    """一档行情"""

    def __init__(self):
        """价格"""
        self.price = 0
        """量"""
        self.volume = 0