# -*- coding: utf-8 -*-
from iqsopenapi.core.events import *
from iqsopenapi.environment import Environment
from iqsopenapi.util import *
import datetime
import json
import time
import uuid

class ExternalNotify(object):
    """外部系统消息通知"""

    def __init__(self, addr, event_bus):
        """构造函数"""

        cfg = websocketCfg()
        cfg.address = addr
        cfg.hbContent = json.dumps({ 'requestType' : 'HeartBeat','reqID' : '' })
        cfg.recvCallback = self.__OnRecv
        cfg.connectedCallback = self.__OnConnect
        self.__wsClient = WebSocketClient(cfg)
        
        event_bus.add_listener(EVENT.On_Trade, self.handle_trade)
        event_bus.add_listener(EVENT.On_Order, self.handle_order)

    def init(self):
        """初始化"""
        if not self.__wsClient.Connect():
            logger.error("user notification connect failed!")
            return False
        self.__wsClient.AutoHeartBeat()
        return True

    def handle_order(self,event):
        if not event or not event.data:
            return
        dict = event.data.__dict__
        dict['requestType'] = 'OnOrder'
        message = json.dumps(dict,ensure_ascii=False, cls=DateTimeEncoder)
        if not self.__Send(message):
            logger.error("send order notify info fail :{0}".format(message))


    def handle_trade(self, event):
        """成交信号"""
        if not event or not event.data:
            return
        dict = event.data.__dict__
        dict['requestType'] = 'OnTrade'
        message = json.dumps(dict,ensure_ascii=False, cls=DateTimeEncoder)
        if not self.__Send(message):
            logger.error("send trade notify info fail :{0}".format(message))

    def __Send(self,msg):
        """消息发送"""
        if not msg:
            return False
        if not self.__wsClient.Send(msg):
            logger.error("send fail:{0}".format(msg))
            return False
        return True

    def __OnRecv(self,msg):
       '''收到消息'''
       if not msg:
           return
       responseType = msg.get("responseType")
       if responseType == 'HeartBeat':
           logger.info("收到心跳消息")
           return 

    def __OnConnect(self):
        """连接"""
        logger.info("连接成功，开始推送用户消息");


 

