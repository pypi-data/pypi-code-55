# -*- coding: utf-8 -*-

from . import wh_setting,api_list

def list():

    api = api_list.user_list
    result = wh_setting.get_requests(api=api)
    return result

def detail(user_idx):
    if type(user_idx) == int:
        user_idx = str(user_idx)

    user_list = list()
    user_list = user_list['users']
    user_detail = []
    for user in user_list:
        if user["user_idx"] == user_idx:
            user_detail = user
            return user_detail
        else:
            print("Not found.")
            return 'Not found.'
