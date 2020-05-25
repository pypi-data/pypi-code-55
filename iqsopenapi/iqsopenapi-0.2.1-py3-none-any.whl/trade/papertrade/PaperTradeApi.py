# -*- coding: utf-8 -*-
from iqsopenapi.models import *
from iqsopenapi.util import *
from iqsopenapi.trade import *
from iqsopenapi.trade.papertrade.message import *
from iqsopenapi.core import *
from iqsopenapi.environment import *
import json
import time
import uuid
import datetime
import traceback
import threading
from copy import copy

class PaperTradeApi(ITradeApi):
    """期货模拟交易"""

    def __init__(self,event_bus):
        """构造函数"""
        super(PaperTradeApi,self).__init__(event_bus)

        self.__event_bus = event_bus

        self.__strategy_id = Environment.get_instance().config.acct_info['strategy_id']
        self.__account_id = Environment.get_instance().config.acct_info['account']

        cfg = websocketCfg()
        cfg.address = Environment.get_instance().get_trademsgaddr()
        cfg.hbContent = json.dumps({ 'requestType' : 'HeartBeat','reqID' : '' })
        cfg.recvCallback = self.__OnRecv
        cfg.connectedCallback = self.__AuotSubscribe
        self.__wsClient = WebSocketClient(cfg)
        self.__subscribes = []
        self.__responseMsgCache = MemCache()

    def Init(self):
        """初始化"""
        if not self.__wsClient.Connect():
            logger.error("paper trade connect failed!")
            return False
        self.__wsClient.AutoHeartBeat()
        if not self.__Subscribe():
            logger.error("paper trade subscribe failed!")
            return False
        return True

    def __AuotSubscribe(self):
        """自动订阅"""
        try:
            if len(self.__subscribes) > 0:
                logger.debug("连接成功，开始订阅...")
                subRet = self.Subscribe(*self.__subscribes)
                logger.debug("连接成功，订阅完成：{0}".format(subRet))
        except Exception as e:
            logger.exception(e)

    def __Subscribe(self):
        id = uuid.uuid1().hex
        req = {"RequestType":RequestType.Subscribe,"ReqID":id,"StrategyId":self.__strategy_id,"TradeAccount":self.__account_id}
        message = json.dumps(req,ensure_ascii=False)
        if not self.__Send(id,message):
            logger.error("Subscribe papertrade send fail:{0}".format(message))
            return False
        logger.info("Subscribe papertrade succeed:{0}".format(message))
        return True

    def __Send(self,id,msg):
        """消息发送"""
        if not msg:
            return False
        if not self.__wsClient.Send(msg):
            logger.error("send fail:{0}".format(msg))
            return False
        i = 0
        while i < 60:
            reply = self.__responseMsgCache.get(id)
            if reply:
                self.__responseMsgCache.delete(id)
                return reply["ErrorNo"] == 0
            i += 1
            time.sleep(0.1)
        return False

    def __OnRecv(self,msg):
        '''收到消息'''
        if not msg:
            return
        responseType = msg.get("rt")
        datas = msg.get("data")
        if responseType == ResponseType.Reply.name:
            self.__responseMsgCache.set(msg.get("ReqID"), msg, 60)
            return
        if responseType == ResponseType.OrderChange.name:
            for item in datas:
                order = self.__ToOrder(item)
                if not order:
                    return
                order_event = Event(EVENT.On_Order,data = order)
                self.__event_bus.publish_event(order_event)
        if responseType == ResponseType.ExecutionReport.name:
            for item in datas:
                trade = self.__ToTrade(item)
                if not trade:
                    return
                trade_event = Event(EVENT.On_Trade,data = trade)
                self.__event_bus.publish_event(trade_event)

    def SendOrder(self,symbol, exchange, orderSide, price, quantity, orderType, offset):
        """下单"""
        if not symbol or symbol == '':
            logger.error("symbol paramter is empty")
            return None
        if not isinstance(quantity, int):
            logger.error("quantity paramter is not int")
            return None

        order = Order()
        order.exchange = exchange
        order.filled = 0
        order.note = ''
        order.offset = offset
        order.order_id = ''
        order.side = orderSide
        order.order_time = datetime.datetime.now()
        order.order_type = orderType
        order.price = price
        order.quantity = quantity
        order.status = OrderStatus.NotSent
        order.symbol = symbol
        order.strategy_id = self.__strategy_id
        order.account_id = self.__account_id
        order_event = Event(EVENT.On_Order,data = order)
        self.__event_bus.publish_event(order_event)

        params = {'symbol':symbol,'exchange':int(exchange),'orderSide':int(orderSide),'price':price,'quantity':quantity,'orderType':int(orderType),'offset':int(offset),'strategyId':self.__strategy_id,'tradeAccount':self.__account_id}
        logger.info("begin sendorder，param:{0}".format(json.dumps(params,ensure_ascii=False)))

        url = Environment.get_instance().get_apiurl('api/PaperTrade/SendOrder')
        resp = httpJsonPost(url, params)
        logger.info("sendorder complated，param:{0},resp:{1}".format(json.dumps(params,ensure_ascii=False),resp))
        if not resp:
            logger.error("response is empty:{0},{1}".format(url,json.dumps(params,ensure_ascii=False)))
            return None
        js = json.loads(resp,encoding='utf-8')

        neworder = copy(order)
        if js.get('error_no') != 0:
            logger.error("sendorder failed:{0},{1},{2}".format(url,json.dumps(params,ensure_ascii=False),resp))
            neworder.status = OrderStatus.Rejected
            neworder.note = js.get('error_info')
        else:
            orderId = js.get('data')['orderId']
            neworder.order_id = str(orderId)
            neworder.status = OrderStatus.Sended
        neworder_event = Event(EVENT.On_Order,data = neworder)
        self.__event_bus.publish_event(neworder_event)
        return neworder

    def CancelOrder(self,order):
        """撤单"""
        if not order or not order.order_id:
            logger.error("invalid order can't cancel")
            return None

        cancelOrder = copy(order)
        cancelOrder.status = OrderStatus.PendingCancel
        cancelOrder.strategy_id = self.__strategy_id
        cancelOrder.account_id = self.__account_id
        order_event = Event(EVENT.On_Order,data = cancelOrder)
        self.__event_bus.publish_event(order_event)

        params = {'orderId':order.order_id,'strategyId':self.__strategy_id,'tradeAccount':self.__account_id}
        logger.info("begin cancelorder，param:{0}".format(json.dumps(params,ensure_ascii=False)))

        url = Environment.get_instance().get_apiurl('api/PaperTrade/CancelOrder')
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("response is empty:{0},{1}".format(url,json.dumps(params,ensure_ascii=False)))
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("cancel order failed:{0},{1},{2}".format(url,json.dumps(params,ensure_ascii=False),resp))

        newCancelOrder = self.GetOrder(order.order_id)

        newCancelOrder_event = Event(EVENT.On_Order,data = newCancelOrder)
        self.__event_bus.publish_event(newCancelOrder_event)

        return newCancelOrder

    def GetAccount(self):
        """获取资产信息"""

        url = Environment.get_instance().get_apiurl('api/PaperTrade/GetAccount')
        params = {'strategyId':self.__strategy_id,'tradeAccount':self.__account_id}
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("response is empty:{0},{1}".format(url,json.dumps(params,ensure_ascii=False)))
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("failed:{0},{1},{2}".format(url,json.dumps(params,ensure_ascii=False),resp))
            return None
        resData = js['data']
        asset = self.__ToAccount(resData)
        return asset

    def GetOrder(self,orderId):
        """根据订单ID号 获取订单详情"""
        orders = self.GetOrders()
        if not orders:
           return None
        for x in orders:
            if x.order_id == orderId:
                return x
        return None

    def GetOpenOrders(self):
        """获取打开的订单"""
        orders = self.GetOrders()
        if not orders:
           return None
        openOrders = []
        for x in orders:
            if x.isopen():
                openOrders.append(x)
        return openOrders

    def GetOrders(self):
        """获取委托"""

        url = Environment.get_instance().get_apiurl('api/PaperTrade/GetOrders')
        params = {'strategyId':self.__strategy_id,'tradeAccount':self.__account_id}
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("response is empty:{0},{1}".format(url,json.dumps(params,ensure_ascii=False)))
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("failed:{0},{1},{2}".format(url,json.dumps(params,ensure_ascii=False),resp))
            return None
        resData = js.get('data')
        if not resData:
            return []
        orders = []
        for item in resData:
            order = self.__ToOrder(item)
            orders.append(order)
        return orders

    def GetPositions(self):
        """获取持仓"""

        url = Environment.get_instance().get_apiurl('api/PaperTrade/GetPositions')
        params = {'strategyId':self.__strategy_id,'tradeAccount':self.__account_id}
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("response is empty:{0},{1}".format(url,json.dumps(params,ensure_ascii=False)))
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("failed:{0},{1},{2}".format(url,json.dumps(params,ensure_ascii=False),resp))
            return None
        resData = js.get('data')
        if not resData:
            return []
        posList = []
        for item in resData:
            pos = self.__ToPos(item)
            posList.append(pos)
        return posList

    def GetTrades(self):
        """获取委托"""

        url = Environment.get_instance().get_apiurl('api/PaperTrade/GetExecutions')
        params = {'strategyId':self.__strategy_id,'tradeAccount':self.__account_id}
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("response is empty:{0},{1}".format(url,json.dumps(params,ensure_ascii=False)))
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("failed:{0},{1},{2}".format(url,json.dumps(params,ensure_ascii=False),resp))
            return None
        resData = js.get('data')
        if not resData:
            return []
        trades = []
        for item in resData:
            trade = self.__ToTrade(item)
            trades.append(trade)
        return trades

    def __ToOrder(self, item):
        order = Order()
        order.exchange = Exchange(item.get('e'))
        order.filled = item['f']
        order.note = item['n']
        order.offset = Offset(item['oft'])
        order.order_id = item['oid']
        order.side = OrderSide(item['osd'])
        order.order_time = datetime.datetime.strptime(item['ote'],'%Y-%m-%d %H:%M:%S')
        order.order_type = OrderType(item['otp'])
        order.price = item['p']
        order.quantity = item['q']
        order.status = OrderStatus(item['ost'])
        order.symbol = item['s']
        order.strategy_id = self.__strategy_id
        order.account_id = self.__account_id
        return order

    def __ToTrade(self, item):
        trade = Trade()
        trade.strategy_id = self.__strategy_id
        trade.account_id = self.__account_id
        trade.exchange = Exchange(item.get('e'))
        trade.symbol = item['s']
        trade.order_id = item['oid']
        trade.trade_id = item['eid']
        trade.side = OrderSide(item['osd'])
        trade.price = item['p']
        trade.offset = Offset(item['oft'])
        trade.quantity = item['q']
        trade.filled_time = datetime.datetime.strptime(item['ft'],'%Y-%m-%d %H:%M:%S')
        return trade

    def __ToPos(self, item):
        pos = Position()
        pos.strategy_id = self.__strategy_id
        pos.account_id = self.__account_id
        pos.symbol = item['s']
        pos.exchange = Exchange(item['e'])
        pos.last_px = item['lp']
        pos.quantity = item['q']
        pos.frozen = item['fz']
        pos.cost = item['c']
        pos.side = PosSide(item['ps'])
        pos.margin = item['m']
        pos.value = item['v']
        pos.today_qty = item['tq']
        pos.today_avl =  item['ta']
        pos.profit = item['pf']
        return pos

    def __ToAccount(self, resData):
        account = Account()
        account.strategy_id = self.__strategy_id
        account.account_id = self.__account_id
        account.total_value = resData['tv']
        account.available = resData['avl']
        account.frozen_cash = resData['fc']
        account.market_value = resData['mv']
        account.margin = resData['m']
        account.begin_balance = resData['bb']
        account.withdraw = resData['wd']
        account.currency = Currency.CNY
        return account

