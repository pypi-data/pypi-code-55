# -*- coding: utf-8 -*-
"""
@Author: YuMinJie
@Date: 2020-05-15 11:16:28
@LastEditTime: 2020-05-15 19:39:31
@LastEditors: ChenXiaolei
@Description: 消息帮助类
"""


import requests


class NoticeHelper(object):

    """
    @description: 群机器人消息
    @last_editors: YuMinJie
    """

    def __init__(self, webhook_key=''):
        if webhook_key != '':
            # 传入webhook秘钥
            self.webhook_key = webhook_key

    def _get_webhook_key(self, webhook_key=''):
        """
        @description: 判断传参webhook_key是否为空字符串，如果为空字符串则从初始化属性获取
        @param index: webhook_key
        @return: webhook_key
        """
        if webhook_key == '':
            if self.webhook_key == '':
                raise Exception("webhook_key is not configured")
            return self.webhook_key
        return webhook_key

    def send_webhook(self, webhook_key='', text='', mentioned_list=[], mentioned_mobile_list=[]):
        """
        @description: webhook_key:webhook秘钥,text:消息文本,传入utf-8,
        @description: mentioned_list:传入工号，或者，@all   1838,122,55,@all
        @description: mentioned_mobile_list:传入手机号，或者,@all      15.......3307,@all  
        @param index: webhook_key
        @return: 企业微信消息
        """

        webhook_key = self._get_webhook_key()
        # 数据合成

        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
        body = {"msgtype": "text", "text": {"content": text,
                                            "mentioned_list": mentioned_list, 'mentioned_mobile_list': mentioned_mobile_list}}

        try:
            response = requests.post(url, json=body, auth=(
                "Content-Type", "application/json"))
        except Exception as ex:
            pass
