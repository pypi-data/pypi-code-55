# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list():
    api = api_list.team_list
    result = wh_setting.get_requests(api=api)
    return result

def user_list(team_idx):
    api = api_list.team_user_list %(team_idx)
    result = wh_setting.get_requests(api=api)
    return result