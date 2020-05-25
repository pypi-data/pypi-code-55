# -*- coding: utf-8 -*-
from iqsopenapi.models.Order import *
from iqsopenapi.util.HttpUtil import *
from iqsopenapi.util.logutil import *
from iqsopenapi.util.DES3Cryptogram import *
from iqsopenapi.trade.realtrade.SupervisionHelper import *
from iqsopenapi.trade.realtrade.Models import *
from iqsopenapi.trade.realtrade.TradeEnums import *
from iqsopenapi.trade.realtrade.ParseManager import *
from iqsopenapi.util.Util import *
from urllib.parse import quote
import os
import string
from iqsopenapi.environment import *
import platform

class RealTradeApiCore:
    """期货交易接口"""

    def __init__(self):
        self.__supervision_helper = SupervisionHelper()
        self.__passwordKey = 'password'
        self.__tradeTokenKey = 'tradeToken'
        
        packType = 1028
        version = '2.4.5.2700'
        self.__appID = "YK_YKCJPC_2.0"

        self.__post_fix = f'?packType={packType}&version={version}&s=py'
        livetradeaddr = Environment.get_instance().get_livetradeaddr()
        self.__qryCounterUrl = self.__encodeUrl(f'{livetradeaddr}allbroker/qrycounterapi.ashx{self.__post_fix}')
        self.__testConnectUrl = self.__encodeUrl(f'gateway/system/testconnect.ashx{self.__post_fix}')
        self.__loginUrl = self.__encodeUrl(f'gateway/login.ashx{self.__post_fix}')
        self.__sendOrderUrl = self.__encodeUrl(f'gateway/sendorder.ashx{self.__post_fix}')
        self.__cancelOrderUrl = self.__encodeUrl(f'gateway/cancelorder.ashx{self.__post_fix}')
        self.__qryEntrustUrl = self.__encodeUrl(f'gateway/qryordertrade.ashx{self.__post_fix}')
        self.__fundUrl = self.__encodeUrl(f'gateway/qryasset.ashx{self.__post_fix}')
        self.__positionUrl = self.__encodeUrl(f'gateway/qryposition.ashx{self.__post_fix}')
        self.__doneUrl = self.__encodeUrl(f'gateway/qrytrade.ashx{self.__post_fix}')

    def GetCounterInfo(self, borkerType):
        """获取指定公司的柜台信息"""
        if(not borkerType): raise Exception("未设置柜台地址!")

        url = self.__qryCounterUrl
        kvp = [kv('brokerType', borkerType)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'GetCounterInfo Url:{url}')
        info = self.__post_crypt_core(url, param, ParseTradeCounterModel)
        if info.ErrorNo != 0:
            self.__wirteError(f'GetCounterInfo, {info.Json}')
            return None
        else: 
            self.__wirteInfo(f'GetCounterInfo, {info.Json}')
            return info
        pass

    def GetCounterApi(self, counter):
        '''自动获取最优的柜台'''
        def pingTime(x):
            ping, result = ExecutedTime(lambda :self.__testConnect(x.ApiAddr))
            if not result: ping = -1
            x.Ping = ping
            return x.Ping > 0
        if(not counter.ApiList or len(counter.ApiList) == 0):raise Exception("获取不到柜台地址!")
        counterApis = list(filter(pingTime, counter.ApiList))
        counterApi = Minimum(counterApis, lambda x:x.Ping)
        return counterApi
        
    def AccountLogin(self, account):
        """登录"""
        borkerType = account.BrokerType
        counterId = account.CounterID
        addr = account.CounterAddr
        userName = account.AccountID
        password = account.PassWord
        super_info = account.SupInfo
        api_id = account.ApiInfoId

        if(not addr): raise Exception("未设置柜台地址!")
        if(super_info.TradeCounter == TradeCounterType.NONE): raise Exception("未设置柜台类型!")

        url = f'{addr}{self.__loginUrl}'
        kvp = [
            kv('brokerType', borkerType), 
            kv('accountID', userName), 
            kv(self.__passwordKey, password), 
            kv('apiInfoId', api_id), 
            kv('AppID', self.__appID), 
            kv('counterID', counterId)]
        js = self.__supervision_helper.SetInfo(super_info)
        kvp[len(kvp):len(js)] = js
        param = self.__getJson(kvp)
        self.__wirteInfo(f'AccountLogin Url:{url}')
        info = self.__post_crypt_core(url, param, ParseLoginResult)
        if info.ErrorNo != 0:
            self.__wirteError(f'AccountLogin, {info.Json}')
            return None
        else: 
            self.__wirteInfo(f'AccountLogin, {info.Json}')
            return info

    def SendOrder(self, order):
        """下单"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__sendOrderUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord), 
            kv('symbol', order.symbol), 
            kv('exchange', order.exchange.name), 
            kv('orderSide', order.side.name), 
            kv('price', order.price), 
            kv('quantity', order.quantity), 
            kv('orderType', order.order_type.value), 
            kv('offset', order.offset.value)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'SendOrder Url:{url}')
        model = self.__post_crypt_core(url, param, ParseSendOrderModel)
        self.__wirteInfo(f'SendOrder, {model.Json}')
        return model

    def CancelOrder(self, orderID):
        """撤单"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__cancelOrderUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord), 
            kv('orderID', orderID)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'CancelOrder Url:{url}')
        model = self.__post_crypt_core(url, param, ParseBaseModel)
        self.__wirteInfo(f'CancelOrder, {model.Json}')
        return model

    def GetAccountFund(self):
        """查询资金"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__fundUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'GetAssetInfo Url:{url}')
        model = self.__post_crypt_core(url, param, ParseUserAssetsModel)
        if model.ErrorNo != 0:
            self.__wirteError(f'GetAssetInfo, {model.Json}')
            return None
        else:
            self.__wirteInfo(f'GetAssetInfo, {model.Json}')
            return model

    def GetEntrustInfos(self, id=None):
        """查询委托"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__qryEntrustUrl}'
        kvp = [kv(self.__tradeTokenKey, account.TradeToken)]
        if id != None:
            kvp[len(kvp):1] = [kv('orderID', id)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'GetEntrustInfos Url:{url}')
        info = self.__post_crypt_core(url, param, ParseEntrustModel)
        if info.ErrorNo != 0:
            self.__wirteError(f'GetEntrustInfos, {info.Json}')
            return None
        else: 
            self.__wirteInfo(f'GetEntrustInfos, {info.Json}')
            return info.EntrustInfos

    def GetPositionInfos(self):
        """查询持仓"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__positionUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord), 
            kv('qryFund', 1)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'GetPositions Url:{url}')
        info = self.__post_crypt_core(url, param, ParsePositionModel)
        if info.ErrorNo != 0:
            self.__wirteError(f'GetPositions, {info.Json}')
            return None
        else: 
            self.__wirteInfo(f'GetPositions, {info.Json}')
            return info.Positions

    def GetTrades(self):
        """获取当日成交"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__doneUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord)]
        param = self.__getJson(kvp)
        self.__wirteInfo(f'GetTrades Url:{url}')
        info = self.__post_crypt_core(url, param, ParseDoneModel)
        if info.ErrorNo != 0:
            self.__wirteError(f'GetTrades, {info.Json}')
            return None
        else: 
            self.__wirteInfo(f'GetTrades, {info.Json}')
            return info.Dones

    def SetUserInfo(self, user):
        self.__user_info = user

    def __testConnect(self, addr):
        url = f"{addr}{self.__testConnectUrl}?&apiAddr={addr}"
        result = httpGet(url)
        js = json.loads(result)
        if("Connected" == js['status']): return js
        else: 
            self.__wirteError(f'TestConnect, {result}')
            return None

    def __encodeUrl(self, url):
        return quote(url, safe=string.printable)

    def __getJson(self, kvp):
        return '{' + ','.join(['"%s":"%s"' % (item.Key, item.Value)  for item in kvp]) + '}'

    def __post_crypt_core(self, url, param, parsecore):
        def parse(x):
            de = decrypt(x)
            return parsecore(json.loads(de))
        en = f'param={encrypt(param)}'
        return parse(httpFormPost(url, en))

    def __wirteError(self, error):
        '''写错误日志'''
        logger.error(error)

    def __wirteInfo(self, info):
        '''写日志'''
        logger.info(info)

    def __getUserInfo(self):
        if(self.__user_info != None): return self.__user_info;
        else: raise Exception("未登录")

if __name__ == '__main__':
    info = { 
    'strategy_id':'1021',
    'account':'10111131',
    'password':'864201',
    'broker_type':1,
    'comp_counter':1,
    }
    brokerType = info['broker_type']
    counterId = info['comp_counter']
    user = UserInfo()
    user.AccountID = info['account']
    user.PassWord = info['password']
    user.BrokerType = brokerType
    user.CounterID = counterId

    api = RealTradeApiCore()
    '''
    counterInfo = api.GetCounterInfo(brokerType)
    counters = list(filter(lambda x:x.CounterId == counterId, counterInfo.CounterList))
    if(not counters or len(counters) == 0):raise Exception("没有对应的柜台id")
    counter = counters[0]
    user.SupInfo.TradeCounter = counter.TradeCounter
    counterApi = api.GetCounterApi(counter)

    user.ApiInfoId = counterApi.ApiInfoId
    user.CounterAddr = counterApi.ApiAddr
    login = api.AccountLogin(user)
    user.TradeToken = login.TradeToken
    '''

    user.SupInfo.TradeCounter = TradeCounterType.HS
    user.ApiInfoId = 19
    user.CounterAddr = 'http://222.178.95.209:11000/'
    user.TradeToken = '0d81ca3e14d84d51a8a7848c8cfbe16b'

    api.SetUserInfo(user)

    #positions = api.GetPositionInfos()
    #entrust = api.GetEntrustInfos()
    #funds = api.GetAccountFund()

    order = Order()
    order.Symbol = 'c2101'
    order.Exchange = Exchange.DCE
    order.OrderSide = OrderSide.Buy
    order.Offset = Offset.Open
    order.OrderType = OrderType.LMT
    order.Price = 1928
    order.Quantity = 1

    if(api.SendOrder(order)): pass

    if(api.CancelOrder(order.OrderId)): pass

    aa = api
