# -*- coding: utf-8 -*-
from iqsopenapi.util import *
from iqsopenapi.util.logutil import *
from iqsopenapi.trade.realtrade.message import *
from iqsopenapi.trade.realtrade.Models import *
import uuid
import threading
import time

class PushQuoteSubscriber(object):
    '''实盘推送'''
    def __init__(self, cfg, strategy_id, user):
        '''初始化websocket'''

        self.__cfg = cfg
        self.__strategy_id = strategy_id
        self.__user_info = user
        self.__recv_callback = cfg.recvCallback
        cfg.recvCallback = self.__OnRecv
        cfg.connectedCallback = self.__AuotSubscribe
        self.__wsClient = WebSocketClient(cfg)

    def Connect(self):
        # 连接websocket
        if not self.__wsClient.Connect():
            self.__wirteError("connect failed!")
            return False
        self.__wsClient.AutoHeartBeat()
        return True

    def __SetAccountInfo(self):
        user = self.__user_info
        req = {
            "requestType":RequestType.TradePushConect.name,
            "reqId":uuid.uuid1().hex,
            "brokerAccount":user.AccountID,
            "counterId":user.CounterID,
            "brokerType":user.BrokerType,
        }
        message = json.dumps(req,ensure_ascii=False)
        if not self.__Send(id,message):
            self.__wirteError("set account info fail :{0}".format(message))
            return False
        return True

    def __Send(self,id,msg):
        """消息发送"""
        if not msg: return False
        if not self.__wsClient.Send(msg):
            self.__wirteError("send fail:{0}".format(msg))
            return False
        return True

    def __OnRecv(self,msg):
        '''收到消息'''
        if not msg: return
        # 心跳消息直接返回
        if msg.get("responseType") == ResponseType.HeartBeat.name: return
        call = self.__recv_callback
        if not call: return
        call(msg)

    def __AuotSubscribe(self):
        """自动订阅"""
        try:
            logger.debug("连接成功，开始推送验证信息...")
            if not self.__SetAccountInfo():
                self.__wirteError("subscribe failed!")
            logger.debug("连接成功，推送验证信息完成")
        except Exception as e:
            logger.exception(e)

    def __wirteError(self, error):
        '''写错误日志'''
        logger.error(error)

    def __wirteInfo(self, info):
        '''写日志'''
        logger.info(info)
