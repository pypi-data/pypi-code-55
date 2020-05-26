# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(project_idx):
    api = api_list.category_list %(project_idx)
    result = wh_setting.get_requests(api=api)
    return result


def create(project_idx,category_name,description=""):
    api = api_list.category_create %(project_idx)
    data = {"category_name":category_name,"description":description}
    result = wh_setting.post_requests(api=api, data=data)
    return result