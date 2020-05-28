# -*- coding: utf-8 -*-
from iqsopenapi.core  import *
from iqsopenapi.util.HttpUtil import *
from iqsopenapi.util.logutil import *
from iqsopenapi.util.DES3Cryptogram import *
from iqsopenapi.trade.ITradeApi import *
from iqsopenapi.models.Order import *
from iqsopenapi.models.Account import *
from iqsopenapi.models.Position import *
from urllib.parse import quote
import string
import json
import time
import uuid
import datetime
from concurrent.futures.thread import ThreadPoolExecutor
from iqsopenapi.trade.realtrade.RealTradeApiCore import *
from iqsopenapi.trade.realtrade.Models import *
from iqsopenapi.trade.realtrade.PushQuoteSubscriber import *
from iqsopenapi.trade.realtrade.message import *
from copy import copy

class RealTradeApi(ITradeApi):
    """期货交易"""

    def __init__(self,event_bus):
        """构造函数"""
        super(RealTradeApi,self).__init__(event_bus)
        
        self.__event_bus = event_bus

        self.__api_core = RealTradeApiCore()
        self.__user_info = None

    def Init(self):
        """初始化"""
        user = UserInfo()

        info = Environment.get_instance().config.acct_info

        # 设置策略id
        strategy_id = info['strategy_id']
        self.__strategy_id = strategy_id

        # 初始化user变量
        brokerType = info['broker_type']
        counterId = info['comp_counter']
        crypt =('crypt' in info) and info['crypt']
        aid = info['account']
        psd = info['password']
        if crypt:
            user.AccountID = decrypt(aid)
            user.PassWord = decrypt(psd)
        else:
            user.AccountID = aid
            user.PassWord = psd
        user.BrokerType = brokerType
        user.CounterID = counterId

        # 按照指定的期货公司id和柜台id获取对应的柜台
        api = self.__api_core
        counterInfo = api.GetCounterInfo(brokerType)
        counters = list(filter(lambda x:x.CounterId == counterId, counterInfo.CounterList))
        if(None ==  counters or len(counters) == 0):raise Exception("没有对应的柜台id")
        counter = counters[0]
        counterApi = api.GetCounterApi(counter)

        # 设置user变量的柜台信息
        user.SupInfo.TradeCounter = counter.TradeCounter
        user.ApiInfoId = counterApi.ApiInfoId
        user.CounterAddr = counterApi.ApiAddr

        # 登录并设置user变量的TradeToken
        self.__wirteInfo('登录!')
        login = api.AccountLogin(user)
        if (None ==  login) : raise Exception('登录失败!')
        user.TradeToken = login.TradeToken

        # 保存user变量
        self.__user_info = user
        api.SetUserInfo(user)

        self.__startReLoginMonitor()
        
        # 设置推送
        self.__wirteInfo('设置推送!')
        cfg = websocketCfg()
        cfg.address = counterApi.wsAddr
        cfg.hbContent = json.dumps({ 'requestType' : RequestType.HeartBeat.name,'reqId' : '' })
        cfg.recvCallback = self.__OnRecv
        subscriber = PushQuoteSubscriber(cfg, strategy_id, user)
        subscriber.Connect()
        self.__subscriber = subscriber

        self.__wirteInfo('初始化完成!')
        return True

    def SendOrder(self, symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        if not symbol or symbol == '':
            self.__wirteError("symbol不能为空")
            return ResultInfo(-1,"symbol不能为空")
        if not isinstance(quantity, int):
            self.__wirteError("quantity必须为整数:{0},{1}".format(quantity,symbol))
            return ResultInfo(-1,"quantity必须为整数:{0},{1}".format(quantity,symbol))
        self.__wirteInfo("准备下单，symbol:{0},exchange:{1},orderSide:{2},offset:{3},orderType:{4},price:{5},quantity:{6}".format(symbol, exchange.name, orderSide, offset.name, orderType.name, price, quantity))
        
        order = Order()
        order.exchange = exchange
        order.filled = 0
        order.note = ''
        order.offset = offset
        order.order_id = ''
        order.side = orderSide
        order.order_time = datetime.now()
        order.order_type = orderType
        order.price = price
        order.quantity = quantity
        order.status = OrderStatus.NotSent
        order.symbol = symbol
        order.strategy_id = self.__strategy_id
        order.account_id = self.__user_info.AccountID
        order_event = Event(EVENT.On_Order,data = order)
        self.__event_bus.publish_event(order_event)
        
        params = {
            'symbol':symbol,
            'exchange':int(exchange),
            'orderSide':int(orderSide),
            'price':price,
            'quantity':quantity,
            'orderType':int(orderType),
            'offset':int(offset),
            'strategyId':self.__strategy_id,
            'tradeAccount':self.__user_info.AccountID
        }
        self.__wirteInfo("begin sendorder，param:{0}".format(json.dumps(params,ensure_ascii=False)))

        model = self.__api_core.SendOrder(order)
        result = model.ErrorNo == 0
        self.__wirteInfo(f'sendorder complated，param:{json.dumps(params,ensure_ascii=False)},resp:{result}')

        neworder = copy(order)
        if(not result):
            neworder.note = model.ErrorInfo
            neworder.status = OrderStatus.Rejected
        else:
            neworder.status = OrderStatus.Sended
            neworder.order_id = str(model.OrderID)
        neworder_event = Event(EVENT.On_Order,data = neworder)
        self.__event_bus.publish_event(neworder_event)
        return neworder

    def CancelOrder(self,order):
        """撤单"""
        if not order or not order.order_id:
            self.__wirteInfo("invalid order can't cancel")
            return None

        cancelOrder = copy(order)
        cancelOrder.status = OrderStatus.PendingCancel
        cancelOrder.strategy_id = self.__strategy_id
        cancelOrder.account_id = self.__user_info.AccountID
        order_event = Event(EVENT.On_Order,data = cancelOrder)
        self.__event_bus.publish_event(order_event)

        params = {'orderId':cancelOrder.order_id,'strategyId':self.__strategy_id,'tradeAccount': self.__user_info.AccountID}
        logger.info("begin cancelorder，param:{0}".format(json.dumps(params,ensure_ascii=False)))
        
        model = self.__api_core.CancelOrder(cancelOrder.order_id)
        result = model.ErrorNo == 0

        newCancelOrder = self.GetOrder(order.order_id)

        newCancelOrder_event = Event(EVENT.On_Order,data = newCancelOrder)
        self.__event_bus.publish_event(newCancelOrder_event)

        return newCancelOrder

    def GetAccount(self):
        """获取资产信息"""
        model = self.__api_core.GetAccountFund()
        if(None == model):raise Exception("获取资产信息失败")
        asset = model.AssetInfo
        asset.strategy_id = self.__strategy_id
        return asset

    def GetOrder(self,orderId):
        """根据内联ID号 获取订单详情"""
        orders = self.GetOrders()
        if not orders: return None
        for x in orders:
            if x.order_id == orderId:
                return x
        return None

    def GetOpenOrders(self):
        """获取打开的订单"""
        orders = self.GetOrders()
        if not orders: return None
        openOrders = []
        for x in orders:
            if x.isopen():
                openOrders.append(x)
        return openOrders

    def GetOrders(self):
        """获取当日委托"""
        orders = self.__api_core.GetEntrustInfos()
        if(None ==  orders):raise Exception("获取当日委托失败")
        for order in orders:
            order.account_id = self.__user_info.AccountID
            order.strategy_id = self.__strategy_id
        return orders

    def GetPositions(self):
        """获取持仓"""
        positions = self.__api_core.GetPositionInfos()
        if(None == positions):raise Exception("获取持仓失败")
        for position in positions:
            position.account_id = self.__user_info.AccountID
            position.strategy_id = self.__strategy_id
        return positions

    def GetTrades(self):
        """获取当日成交"""
        dones = self.__api_core.GetTrades()
        if(None == dones):raise Exception("获取当日成交失败")
        for done in dones:
            done.account_id = self.__user_info.AccountID
            done.strategy_id = self.__strategy_id
        return dones

    def __OnRecv(self,msg):
        '''收到消息'''
        if not msg:
            return
        if msg.get("responseType") != ResponseType.TradePush.name:
            return

        logger.info(msg)
        msg_type = MsgType(msg.get('msgType'))
        data = msg.get('metaData')

        if msg_type == MsgType.Order:
            order = self.__ToOrder(data)
            if not order:
                return
            order_event = Event(EVENT.On_Order,data = order)
            self.__event_bus.publish_event(order_event)
        if msg_type == MsgType.Trade:
            trade = self.__ToTrade(data)
            if not trade:
                return
            trade_event = Event(EVENT.On_Trade,data = trade)
            self.__event_bus.publish_event(trade_event)

    def __ToOrder(self, item):
        data = json.loads(item)
        order = Order()
        order.exchange = Exchange(data['exchange'])
        order.order_time = datetime.strptime(data['orderTime'],'%Y-%m-%d %H:%M:%S')
        #order.filled = 
        order.note = str(data['errorMsg'])
        order.offset = Offset(data['offset'])
        order.side = OrderSide.__dict__[data['orderSide']]
        order.order_type = OrderType(data['orderType'])
        order.price = float(data['price'])
        order.quantity = int(data['quantity'])
        order.status = OrderStatus(data['status'])
        order.symbol = str(data['symbol'])
        order.strategy_id = self.__strategy_id
        order.account_id = self.__user_info.AccountID
        order.order_id = data['orderId']
        if ('errorNo' in data):
            errorNo = int(data['errorNo'])
            if(errorNo != 0 and 'errorMsg' in data):
                order.note = data['errorMsg']
        return order

    def __ToTrade(self, item):
        data = json.loads(item)
        trade = Trade()
        trade.strategy_id = self.__strategy_id
        trade.account_id = self.__user_info.AccountID
        trade.exchange = Exchange(data['exchange'])
        trade.symbol = str(data['symbol'])
        trade.order_id = str(data['orderId'])
        trade.trade_id = str(data['tradeId'])
        trade.side = OrderSide.__dict__[data['orderSide']]
        trade.price = float(data['price'])
        trade.offset = Offset(data['offset'])
        trade.quantity = int(data['filled'])
        trade.filled_time = datetime.strptime(data['filledTime'],'%Y-%m-%d %H:%M:%S')
        return trade

    def __startReLoginMonitor(self):
        model = self.__api_core.GetAccountFund()
        if(self.__needReLogin(model)):
            self.__reLogin()
        Timer(30, self.__startReLoginMonitor).start()
    
    def __reLogin(self):
        self.__wirteInfo('重新登录!')
        api = self.__api_core
        user = self.__user_info
        login = api.AccountLogin(user)
        if (None ==  login) : return
        user.TradeToken = login.TradeToken
        self.__user_info = user
        api.SetUserInfo(user)

    def __needReLogin(self, model):
        return model != None and model.ErrorNo == 1

    def __wirteError(self, error):
        '''写错误日志'''
        logger.error(error)

    def __wirteInfo(self, info):
        '''写日志'''
        logger.info(info)

def __object_2_json(x):
    return x.__dict__

if __name__ == '__main__':
    """测试"""
    try:
        raise Exception('未测试')
        #logutil.setLogPath("d:/logs/")
        event_bus = EventBus()
        trade_api = RealTradeApi(event_bus)
        trade_api.Init()

        position = trade_api.GetPositions()
        orders = trade_api.GetOrders()
        assets = trade_api.GetAccount()
        trades = trade_api.GetTrades()

        opens = trade_api.GetOpenOrders()
        if(opens and len(opens) > 0):
            for open in opens:
                cancel = trade_api.CancelOrder(open.order_id)
                if (None == cancel) : raise Exception("撤单失败")

        symbol = 'c2007'
        exchange = Exchange.DCE
        orderSide = OrderSide.Buy
        offset = Offset.Open
        orderType = OrderType.LMT
        price = 1955
        quantity = 1

        sendOrder = trade_api.SendOrder(symbol, exchange, orderSide, price, quantity, orderType, offset)
        if (None == sendOrder) : raise Exception("下单失败")
        aa = price

    except Exception as e:
        print(e)
    pass
