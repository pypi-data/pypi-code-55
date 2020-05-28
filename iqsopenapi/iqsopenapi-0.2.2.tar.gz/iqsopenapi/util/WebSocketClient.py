# -*- coding: utf-8 -*-
from iqsopenapi.util import *
from websocket import *
from queue import Queue
import datetime
import threading
import time
import json
import ssl

class websocketCfg(object):
    """websocket配置信息"""

    def __init__(self):
        """地址"""
        self.address = ""

        """心跳间隔"""
        self.hbInternal = 5

        """超时"""
        self.keepAliveTimeout = 30

        """心跳内容"""
        self.hbContent = None

        """收到数据回调"""
        self.recvCallback = None

        """"连接成功回调"""
        self.connectedCallback = None

class WebSocketClient(object):
    """WebSocket"""

    def __init__(self,cfg):
        """构造函数"""

        #连接地址
        self.config = cfg
        #websocket
        self.__wsclinet = None
        #上次活跃时间
        self.__lastActiveTime = datetime.datetime.now()
        #缓存队列
        self.__unhandledQueue = Queue()
        t = threading.Thread(target=self.__HandleMsg)
        t.start()
        t1 = threading.Thread(target=self.__ReceiveMsg)
        t1.start()
        self._hasAutoHeartBeat = False
    
    def Connect(self):
        """连接"""
        if self.IsAvaliable():
            return True
        logger.debug("begin connect:{0}".format(self.config.address))
        self.__wsclinet = create_connection(self.config.address,  sslopt={"cert_reqs": ssl.CERT_NONE})
        logger.debug("conenect succeed:{0},state:{1}".format(self.config.address,self.__wsclinet.connected))
        self.__lastActiveTime = datetime.datetime.now()
        if self.config.connectedCallback:
            self.config.connectedCallback()
        return True

    def AutoHeartBeat(self):
        """启动自动心跳功能"""
        if self._hasAutoHeartBeat:
            return
        self._hasAutoHeartBeat = True
        t2 = threading.Thread(target=self.__AutoHeartBeat)
        t2.start()

    def IsAvaliable(self):
        """判断是否是有效连接"""
        if not self.__wsclinet:
            return False
        if not self.__wsclinet.connected:
            return False
        if(datetime.datetime.now() - self.__lastActiveTime).seconds > self.config.keepAliveTimeout:
            return False
        return True

    def Send(self,content):
        """发送消息"""
        if not content:
            return None
        if not self.IsAvaliable():
            return None
        data = bytes(content, encoding = "utf8") 
        return self.__wsclinet.send(data)
 
    def __ReceiveMsg(self):
        """接收消息"""
        while True:
            try:
                 if not self.IsAvaliable():
                     time.sleep(1)
                     continue
                 msg = self.__wsclinet.recv()
                 logger.debug("receive msg from:{0},msg:{1}".format(self.config.address,msg))
                 self.__lastActiveTime = datetime.datetime.now()
                 self.__unhandledQueue.put(msg)
            except Exception as e:
                logger.exception(e)
                time.sleep(1)

    def __HandleMsg(self):
        """处理消息"""
        while True:
            try:
                msg = self.__unhandledQueue.get()
                if not msg:
                    time.sleep(1)
                    continue
                self.__RaiseMessage(msg)
            except Exception as e:
                logger.exception(e)
                time.sleep(1)
    
    def __AutoHeartBeat(self):
        """心跳"""
        if not self.config.hbContent:
            logger.warn("heart beat content is None, skip heart beat:{0}".format(self.config.address))
            return
        logger.debug("start heart beat:{0}...".format(self.config.address))
        while True:
            time.sleep(self.config.hbInternal)
            try:
                if not self.IsAvaliable():
                    logger.error("connect is not avaliable,{0},{1}".format(self.config.address,self.__lastActiveTime))
                    self.__Close()
                    logger.info("begin reconnect:{0}".format(self.config.address))
                    self.Connect()
                    logger.info("reconnect is succeed:{0}".format(self.config.address))
                self.Send(self.config.hbContent)
                logger.debug("send heart beat:{0}".format(self.config.address))
            except Exception as e:
                logger.exception(e)
                self.__Close()

    def __RaiseMessage(self,msg):
        if not msg:
            return
        logger.debug("receive message:{0},{1}".format(msg,self.config.address))
        data = json.loads(msg,encoding='utf-8')
        self.config.recvCallback(data)
    
    def __Close(self):
        try:
            if self.__wsclinet:
                self.__wsclinet.close()
            self.__wsclinet = None
        except Exception as e:
            logger.exception(e)
        
        
if __name__ == '__main__':
    cfg = websocketCfg()
    cfg.address = "wss://dev_apigateway.inquantstudio.com/usermsg/"
    cfg.hbContent = json.dumps({ 'requestType' : 'HeartBeat','reqID' : '' })
    cfg.recvCallback = lambda msg:logger.info(msg)

    ws = WebSocketClient(cfg)
    ws.Connect()
