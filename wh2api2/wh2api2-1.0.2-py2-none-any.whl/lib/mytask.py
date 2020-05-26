# -*- coding: utf-8 -*-

from . import wh_setting, api_list


def todo(observed_user_idx=""):
    api = api_list.mytask_todo
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result

def inprogress(last="",observed_user_idx=""):
    api = api_list.mytask_inprogress %(last)
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result

def done(observed_user_idx=""):
    api = api_list.mytask_done
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result

def cc(last="",observed_user_idx=""):
    api = api_list.mytask_cc %(last)
    result = wh_setting.get_requests(api=api,observed_user_idx = observed_user_idx)
    return result