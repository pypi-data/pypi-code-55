# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(project_idx,category_idx):
    api = api_list.asset_list %(project_idx,category_idx)
    result = wh_setting.get_requests(api=api)
    return result

def create(project_idx,category_idx,asset_name,description="",status_idx="1"):
    api = api_list.asset_create %(project_idx,category_idx)
    data = {"asset_name":asset_name,"description":description,"status_idx":status_idx}
    result = wh_setting.post_requests(api=api,data=data)
    return result

def thumbnail_update(project_idx,asset_idx,thumbnail_path):
    api = api_list.asset_thumbnail_up %(project_idx,asset_idx)
    thumbnail = open(thumbnail_path,'rb')
    files = {"attached":thumbnail}
    result = wh_setting.post_requests(api=api,files=files)
    return result

def overview(project_idx,category_idx=""):
    if category_idx == "":
        api = api_list.asset_overview_all %(project_idx)
    else :
        api = api_list.asset_overview_category %(project_idx,category_idx)
    result = wh_setting.get_requests(api=api)
    return result