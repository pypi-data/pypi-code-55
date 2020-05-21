# -*- coding: utf-8 -*- 
from enum import IntEnum

class IMessage(object):
    """消息"""

    def __init__(self):
        pass

class IRequestMessage(IMessage):
    """请求消息"""

    def __init__(self):
        """消息类型"""
        self.RequestType = RequestType.HeartBeat

        """请求编号"""
        self.ReqID  = ""

class RequestMessage(IRequestMessage):
    """请求消息"""

    def __init__(self):
        """消息类型"""
        self.RequestType = RequestType.HeartBeat

        """请求编号"""
        self.ReqID = ""

class IResponseMessage(IMessage):
    """应答消息"""

    def __init__(self):
        """消息类型"""
        self.ResponseType = ResponseType.HeartBeat

class ResponseMessage(IResponseMessage):
    """应答消息"""
    
    def __init__(self):
        """消息类型"""
        self.ResponseType = ResponseType.HeartBeat

        """数据"""
        self.Data = None
    

class RequestType(IntEnum):
    """行情消息类型"""
    
    """心跳包消息"""
    HeartBeat = 0

    """订阅"""
    Subscribe = 1

    """取消订阅"""
    Unsubscribe= 2

class ResponseType(IntEnum):
    """响应消息类型"""

    """心跳包消息"""
    HeartBeat = 0 

    """请求回复消息"""
    Reply = 1

    """逐笔行情"""
    TickData  = 99

    """周期行情"""
    KlineData = 100
