# -*- coding: utf-8 -*-
from iqsopenapi.marketdata.message import *

class SubscribeReq(RequestMessage):
    """订阅请求"""
    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.Subscribe

        """订阅列表"""
        self.Subscribes = []

