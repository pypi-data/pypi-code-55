# -*- coding: UTF-8 -*-

import json

import requests


# 通过传入一个工号，将消息推送到个人
def send_message(users: list, content):
    response = requests.post(
        url='http://msg.inner-yuceyi.com/cf-wechat/send-by-id',
        data={
            'appId': '06048',
            'users': users,
            'content': content
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded '
        }
    )
    print(response.text)


# EOR机器人消息
def group_robot(url, content):
    requests.post(
        url=url,
        data=json.dumps(
            {
                "msgtype": "text",
                "text": {
                    "content": content,
                }
            }
        ),
        headers={
            'Content-Type': 'application/json'
        })
