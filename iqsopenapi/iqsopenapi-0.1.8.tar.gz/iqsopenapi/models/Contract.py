# -*- coding: utf-8 -*- 

from datetime import *
from enum import IntEnum

class Contract(object):
    """合约信息"""

    def __init__(self):
        """代码"""
        self.symbol = ""

        """名称"""
        self.contract_name = ""

        """交易所"""
        self.exchange = Exchange.UnKnow

        """投资品种类型"""
        self.contract_type = ContractType.UnKnow

        """每股手数"""
        self.lots = 1

        """最小价差"""
        self.step = 0

        """到期日"""
        self.expire_date = datetime.now()

        """行权价"""
        self.strike_px = 0.0

        """期权类型 P:Put C:Call"""
        self.right = ""

        """上市日期"""
        self.list_date = datetime.now()

        """币种"""
        self.currency = Currency.CNY

        """交易时间"""
        self.trade_times = []

class tradeTime(object):
    """交易时间"""

    def __init__(self):
        """开始时间"""
        self.begin = ""

        """结束时间"""
        self.end = ""

class ContractType(IntEnum):
        """合约类型"""

        """未知"""
        UnKnow = 0
        """股票"""
        Stock = 1
        """期货"""
        Future = 2
        """期权"""
        Option = 3

class Exchange(IntEnum):
        """交易所"""

        """未知"""
        UnKnow = 0
        """上交所"""
        SHSE = 1
        """深交所"""
        SZSE = 2
        """中金所"""
        CFFEX = 3
        """上期所"""
        SHFE = 4
        """大商所"""
        DCE = 5
        """郑商所"""
        CZCE = 6
        """港交所"""
        HKSE = 7
        """纳斯达克"""
        NASDAQ = 8
        """纽约证券交易所"""
        NYSE = 9
        """全美证券交易所"""
        AMEX = 10
        """新三板"""
        SBSE = 11
        """伦敦商品交易所"""
        LME = 12
        """马来西亚衍生产品交易所"""
        BMD = 13
        """东京商品交易所"""
        TOCOM = 14
        """上海国际能源交易中心"""
        INE = 15

class Currency(IntEnum):
        """币种"""
        
        """人民币"""
        CNY = 0
        """美元"""
        USD = 1
        """港币"""
        HKD = 2