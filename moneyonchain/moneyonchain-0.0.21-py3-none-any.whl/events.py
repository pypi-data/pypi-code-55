"""
                    GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 THIS IS A PART OF MONEY ON CHAIN PACKAGE
 by Martin Mulone (martin.mulone@moneyonchain.com)

"""

import logging
from web3 import Web3
from web3.exceptions import BlockNotFound
import datetime


class BaseEvent(object):
    name = "BaseEvent"
    hours_delta = 0

    def print_row(self):
        print('\t'.join(self.columns()))
        print('\t'.join(str(v) for v in self.row()))


class MoCExchangeRiskProMint(BaseEvent):

    name = "RiskProMint"

    def __init__(self, connection_manager, event):

        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'Amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCExchangeRiskProWithDiscountMint(BaseEvent):
    name = "RiskProWithDiscountMint"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        ts = connection_manager.block_timestamp(self.blockNumber)
        dt = ts - datetime.timedelta(hours=self.hours_delta)
        self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        self.riskProTecPrice = Web3.fromWei(event['args']['riskProTecPrice'], 'ether')
        self.riskProDiscountPrice = Web3.fromWei(event['args']['riskProDiscountPrice'], 'ether')
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'riskProTecPrice', 'riskProDiscountPrice', 'amount']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                format(float(self.riskProTecPrice), '.18f'),
                format(float(self.riskProDiscountPrice), '.18f'),
                format(float(self.amount), '.18f')]


class MoCExchangeRiskProRedeem(BaseEvent):
    name = "RiskProRedeem"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCExchangeStableTokenMint(BaseEvent):
    name = "StableTokenMint"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCExchangeStableTokenRedeem(BaseEvent):
    name = "StableTokenRedeem"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'amount', 'reserveTotal', 'commission', 'reservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCExchangeFreeStableTokenRedeem(BaseEvent):
    name = "FreeStableTokenRedeem"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.interests = Web3.fromWei(event['args']['interests'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Account', 'Amount', 'ReserveTotal', 'Commission', 'Interests', 'ReservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.interests), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCExchangeRiskProxMint(BaseEvent):
    name = "RiskProxMint"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.bucket = 'X2'
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.interests = Web3.fromWei(event['args']['interests'], 'ether')
        self.leverage = Web3.fromWei(event['args']['leverage'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Bucket', 'Account', 'Amount', 'Reserve Total', 'Interests',  'Leverage',  'Commission',  'Reserve Price']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.bucket,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.interests), '.18f'),
                format(float(self.leverage), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCExchangeRiskProxRedeem(BaseEvent):
    name = "RiskProxRedeem"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.bucket = 'X2'
        self.account = event['args']['account']
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')
        self.reserveTotal = Web3.fromWei(event['args']['reserveTotal'], 'ether')
        self.interests = Web3.fromWei(event['args']['interests'], 'ether')
        self.leverage = Web3.fromWei(event['args']['leverage'], 'ether')
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'Bucket', 'Account', 'Amount', 'Reserve Total', 'Interests',  'Leverage',  'Commission',  'Reserve Price']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.bucket,
                self.account,
                format(float(self.amount), '.18f'),
                format(float(self.reserveTotal), '.18f'),
                format(float(self.interests), '.18f'),
                format(float(self.leverage), '.18f'),
                format(float(self.commission), '.18f'),
                format(float(self.reservePrice), '.18f')]


# SETTLEMENT

class MoCSettlementRedeemRequestProcessed(BaseEvent):
    name = "RedeemRequestProcessed"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''

        self.redeemer = event['args']['redeemer']
        self.commission = Web3.fromWei(event['args']['commission'], 'ether')
        self.amount = Web3.fromWei(event['args']['amount'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº',  'Timestamp', 'Account', 'Commission', 'Amount']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.redeemer,
                format(float(self.commission), '.18f'),
                format(float(self.amount), '.18f')]


class MoCSettlementSettlementRedeemStableToken(BaseEvent):
    name = "SettlementRedeemStableToken"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''

        self.queueSize = event['args']['queueSize']
        self.accumCommissions = Web3.fromWei(event['args']['accumCommissions'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'queueSize', 'accumCommissions', 'reservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.queueSize,
                format(float(self.accumCommissions), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCSettlementSettlementCompleted(BaseEvent):
    name = "SettlementCompleted"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''
        self.commissionsPayed = Web3.fromWei(event['args']['commissionsPayed'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp', 'commissionsPayed']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                format(float(self.commissionsPayed), '.18f')]


class MoCSettlementSettlementDeleveraging(BaseEvent):
    name = "SettlementDeleveraging"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''

        self.leverage = Web3.fromWei(event['args']['leverage'], 'ether')
        self.riskProxPrice = Web3.fromWei(event['args']['riskProxPrice'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')
        self.startBlockNumber = Web3.fromWei(event['args']['startBlockNumber'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº',  'Timestamp', 'leverage', 'riskProxPrice', 'reservePrice', 'startBlockNumber']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                format(float(self.leverage), '.18f'),
                format(float(self.riskProxPrice), '.18f'),
                format(float(self.reservePrice), '.18f'),
                self.startBlockNumber]


class MoCSettlementSettlementStarted(BaseEvent):
    name = "SettlementStarted"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''

        self.stableTokenRedeemCount = event['args']['stableTokenRedeemCount']
        self.deleveragingCount = event['args']['deleveragingCount']
        self.riskProxPrice = Web3.fromWei(event['args']['riskProxPrice'], 'ether')
        self.reservePrice = Web3.fromWei(event['args']['reservePrice'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº',  'Timestamp', 'stableTokenRedeemCount', 'deleveragingCount', 'riskProxPrice', 'reservePrice']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.stableTokenRedeemCount,
                self.deleveragingCount,
                format(float(self.riskProxPrice), '.18f'),
                format(float(self.reservePrice), '.18f')]


class MoCSettlementRedeemRequestAlter(BaseEvent):
    name = "RedeemRequestAlter"

    def __init__(self, connection_manager, event):
        self.blockNumber = event['blockNumber']
        try:
            ts = connection_manager.block_timestamp(self.blockNumber)
            dt = ts - datetime.timedelta(hours=self.hours_delta)
            self.timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        except BlockNotFound:
            self.timestamp = ''

        self.redeemer = event['args']['redeemer']
        self.isAddition = event['args']['isAddition']
        self.delta = Web3.fromWei(event['args']['delta'], 'ether')

    @staticmethod
    def columns():
        columns = ['Block Nº', 'Timestamp',  'address', 'isAddition', 'delta']
        return columns

    def row(self):
        return [self.blockNumber,
                self.timestamp,
                self.redeemer,
                self.isAddition,
                format(float(self.delta), '.18f')]
