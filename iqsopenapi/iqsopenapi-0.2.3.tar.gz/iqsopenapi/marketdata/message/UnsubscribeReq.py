# -*- coding: utf-8 -*-
from iqsopenapi.marketdata.message import *

class UnsubscribeReq(RequestMessage):

    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.Unsubscribe

        """取消订阅列表"""
        self.Unsubscribes = []