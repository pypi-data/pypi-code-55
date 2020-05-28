# -*- coding: utf-8 -*- 
from iqsopenapi.trade.papertrade.message.IMessage import *

class HeartBeatReq(RequestMessage):
    """心跳请求"""

    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.HeartBeat
