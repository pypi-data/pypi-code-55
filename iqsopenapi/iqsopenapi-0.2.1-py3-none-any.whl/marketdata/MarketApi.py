# -*- coding: utf-8 -*-
from iqsopenapi.models import *
from iqsopenapi.util import *
from iqsopenapi.marketdata.message import *
from iqsopenapi.marketdata.IMarketApi import *
from iqsopenapi.core import *
from iqsopenapi.environment import *
import json
import time
import uuid
import iqsopenapi.util.logutil
import datetime
import traceback
import threading


class MarketApi(IMarketApi):
    """行情接口"""

    def __init__(self,event_bus):
        """构造函数"""
        super(MarketApi,self).__init__(event_bus)

        self.__event_bus = event_bus

        cfg = websocketCfg()
        cfg.address = Environment.get_instance().get_quoteaddr()
        cfg.hbContent = json.dumps({ 'requestType' : 'HeartBeat','reqID' : '' })
        cfg.recvCallback = self.__OnRecv
        cfg.connectedCallback = self.__AuotSubscribe
        self.__wsClient = WebSocketClient(cfg)
        self.__subscribes = []
        self.__responseMsgCache = MemCache()

    def Init(self):
        """初始化"""
        if not self.__wsClient.Connect():
            logger.error("market connect failed!")
            return False
        self.__wsClient.AutoHeartBeat()
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

    def __OnRecv(self,msg):
        '''收到行情消息'''

        if not msg:
            return
        responseType = msg.get("rt")
        datas = msg.get("data")
        if responseType == ResponseType.Reply.name:
            self.__responseMsgCache.set(msg.get("ReqID"), msg, 60)
            return
        if responseType == ResponseType.TickData.name:
            for item in datas:
                tick = self.__ToTickData(item)
                if not tick:
                    return
                tick_event = Event(EVENT.On_Tick,data = tick)
                self.__event_bus.publish_event(tick_event)
        if responseType == ResponseType.KlineData.name:
            for item in datas:
                bar = self.__ToBar(item)
                if not bar:
                    return
                bar_event = Event(EVENT.On_Bar,data = bar)
                self.__event_bus.publish_event(bar_event)

    def GetSubscibes(self):
        """获取订阅列表"""
        return self.__subscribes

    def Subscribe(self,*subInfos):
        """行情订阅"""
        if not subInfos:
            logger.error('订阅参数不能为空')
            return False
        if not self.__wsClient.IsAvaliable():
            logger.error('行情未连接')
            return False
        req = SubscribeReq()
        req.ReqID = uuid.uuid1().hex
        req.RequestType = RequestType.Subscribe
        req.Subscribes = subInfos
        message = json.dumps(req.__dict__,ensure_ascii=False)
        if not self.__Send(req.ReqID,message):
            logger.error("Subscribe market send fail:{0}".format(message))
            return False
        logger.info("Subscribe market succeed:{0}".format(message))
        for x in subInfos:
            if x not in self.__subscribes:
                self.__subscribes.append(x)
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


    def Unsubscribe(self,*subInfos):
        """取消订阅"""
        if not subInfos:
            logger.error('订阅参数不能为空')
            return False
        if not self.__wsClient.IsAvaliable():
            logger.error('行情未连接')
            return False
        req = UnsubscribeReq()
        req.ReqID = uuid.uuid1().hex
        req.RequestType = RequestType.Unsubscribe
        req.Unsubscribes = subInfos
        message = json.dumps(req.__dict__,ensure_ascii=False)
        if not self.__Send(req.ReqID,message):
            logger.error("Unsubscribe market send fail:{0}".format(message))
            return False
        logger.info("Unsubscribe market succeed:{0}".format(message))
        for x in subInfos:
            if x in self.__subscribes:
                self.__subscribes.remove(x)
        return True

    def GetHisBar(self, symbol, exchange, barType, startTime, endTime):
        """获取历史K线数据"""
        if not symbol:
            logger.error("合约代码不能为空")
            return None
        url = Environment.get_instance().get_apiurl('api/MarketData/GetHisBar')
        params = {'symbol':symbol,'exchange':exchange,'dataType':barType,'begin':startTime,'end':endTime}
        resp = httpJsonPost(url,params) 
        strParams = json.dumps(params,ensure_ascii=False)
        if not resp:
            logger.error("response：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            return None
        result = []
        for x in data:
            bar = self.__ToBar(x)
            result.append(bar)
        return result

    def GetLastBar(self, symbol, exchange, barType, count):
        """获取历史K线数据"""
        if not symbol:
            logger.error("合约代码不能为空")
            return None
        url = Environment.get_instance().get_apiurl('api/MarketData/GetLastBar')
        params = {'symbol':symbol,'exchange':exchange,'dataType':barType,'count':count}
        resp = httpJsonPost(url,params) 
        strParams = json.dumps(params,ensure_ascii=False)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            return None
        result = []
        for x in data:
            bar = self.__ToBar(x)
            result.append(bar)
        return result

    def GetHisTick(self, symbol, exchange, startTime, endTime):
        """获取历史TICK数据"""
        if not symbol:
            logger.error("合约代码不能为空")
            return None
        url = Environment.get_instance().get_apiurl('api/MarketData/GetHisTick')
        params = {'symbol':symbol,'exchange':exchange,'begin':startTime,'end':endTime}
        resp = httpJsonPost(url,params) 
        strParams = json.dumps(params,ensure_ascii=False)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            return None
        result = []
        for x in data:
            tick = self.__ToTickData(x)
            result.append(tick)
        return result

    def GetLastTick(self, symbol, exchange, count):
        """获取历史TICK数据"""
        if not symbol:
            logger.error("合约代码不能为空")
            return None
        url = Environment.get_instance().get_apiurl('api/MarketData/GetLastTick')
        params = {'symbol':symbol,'exchange':exchange,'count':count}
        resp = httpJsonPost(url,params) 
        strParams = json.dumps(params,ensure_ascii=False)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            return None
        result = []
        for x in data:
            tick = self.__ToTickData(x)
            result.append(tick)
        return result

    def __ToBar(self,data):
        #消息长度可能会增加
        if not data:
            return None
        bar = BarData()
        bar.symbol = data.get("s")
        bar.exchange = Exchange[data.get("e")]
        bar.bar_type = int(data.get("d"))
        bar.local_time = datetime.datetime.strptime(str(data.get("t")),'%Y%m%d%H%M%S') 
        bar.pre_close = float(data.get("pc"))
        bar.open = float(data.get("o"))
        bar.high = float(data.get("h"))
        bar.low = float(data.get("l"))
        bar.close = float(data.get("c"))
        bar.volume = int(data.get("v"))
        bar.turnover = float(data.get("a"))
        bar.open_interest = int(data.get("oi"))
        bar.settlement = float(data.get("sp"))
        return bar

    def __ToTickData(self,data):
        if not data:
            return None
        tick = TickData()
        tick.symbol = data.get("s")
        tick.exchange = Exchange[data.get("e")]
        tick.local_time = datetime.datetime.strptime(str(data.get("t")),'%Y%m%d%H%M%S') 
        tick.last = float(data.get("px"))
        tick.open = float(data.get("o"))
        tick.high = float(data.get("h"))
        tick.low = float(data.get("l"))
        tick.upper_limit = float(data.get("up"))
        tick.lower_limit = float(data.get("dw"))
        tick.pre_close = float(data.get("pc"))
        tick.volume = int(data.get("v"))
        tick.open_interest = int(data.get("oi"))
        tick.settlement = float(data.get("sp"))
        tick.turnover = float(data.get("a"))
        bids = data.get("bid")
        for x in bids:
            unit = LevelUnit()
            unit.price = float(x['p'])
            unit.volume = int(x['v'])
            tick.bids.append(unit)
        asks = data.get("ask")
        for x in asks:
            unit = LevelUnit()
            unit.price = float(x['p'])
            unit.volume = int(x['v'])
            tick.asks.append(unit)
        return tick

if __name__ == '__main__':

    from iqsopenapi.core.events import *

    config = {
      "runtime": "DEBUG"
    }

    environment = Environment(config)

    event_bus = EventBus()

    event_bus.add_listener(EVENT.On_Bar,lambda msg:logger.info('bar:{0},{1},{2}'.format(msg.data.Symbol,msg.data.LocalTime,msg.data.ClosePx)))

    event_bus.add_listener(EVENT.On_Tick,lambda msg:logger.info('tick:{0},{1},{2}'.format(msg.data.Symbol,msg.data.LocalTime,msg.data.LastPx)))

    api = MarketApi(event_bus)
    api.Init()
    
    init_event = Event(EVENT.On_Init)
    event_bus.publish_event(init_event)

    event_bus.start()

    ret1 = api.Subscribe("rb2010.SHFE.TICK.0","rb2010.SHFE.BAR.300","rb2005.SHFE.TICK.0")

    ret2 = api.Unsubscribe("rb2005.SHFE.TICK.0")

    ret3 = api.GetHisBar("rb2010",Exchange.SHFE,60,"20200423","20200424")

    ret4 = api.GetHisTick("rb2010",Exchange.SHFE,"20200423","20200424")

    ret5 = api.GetLastBar("rb2010",Exchange.SHFE,60,100)

    ret6 = api.GetLastTick("rb2010",Exchange.SHFE,100)

    pass