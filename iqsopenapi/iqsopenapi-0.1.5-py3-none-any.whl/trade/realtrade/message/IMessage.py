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

    ''' 设置交易账号等信息 '''
    TradePushConect = 1

class ResponseType(IntEnum):
    """响应消息类型"""

    """心跳包消息"""
    HeartBeat = 0 

    ''' 交易推送 '''
    TradePush = 1

class MsgType(IntEnum):
    ''' 交易推送消息类型 '''

    ''' 委托回报 '''
    Order = 1

    ''' 成交回报 '''
    Trade = 2

    ''' 止盈止损设置 '''
    StopPriceSeting = 3

    ''' 条件单触发 '''
    ConditionOrderTrigger = 4

    ''' 止盈止损触发 '''
    StopOrderTrigger = 5