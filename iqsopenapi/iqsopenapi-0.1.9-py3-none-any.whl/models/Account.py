# -*- coding: utf-8 -*-
from enum import IntEnum
from iqsopenapi.models.Contract import *

class Account(object):
    """资产信息"""

    def __init__(self):
        
        """策略编号"""
        self.strategy_id = ""

        """账户编号"""
        self.account_id = ""

        """总权益"""
        self.total_value = 0.0

        """可用资金"""
        self.available = 0.0

        """冻结资金"""
        self.frozen_cash = 0.0

        """总市值"""
        self.market_value = 0.0

        """保证金"""
        self.margin = 0.0

        """期初权益"""
        self.begin_balance = 0.0

        """可提资金"""
        self.withdraw = 0.0

        """币种"""
        self.currency = Currency.CNY


