# -*- coding: utf-8 -*- 
from iqsopenapi.trade.papertrade.message.IMessage import *

class ReplyResp(ResponseMessage):
    """消息回复"""

    def __init__(self,errorNo,errorInfo):
        """错误代码"""
        self.ErrorNo = errorNo

        """错误消息"""
        self.ErrorInfo = errorInfo

        """应答类型"""
        self.ResponseType = ResponseType.Reply

        """请求编号"""
        self.ReqID = ""



