# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(project_idx,episode_idx,sequence_idx):
    api = api_list.shot_list %(project_idx,episode_idx,sequence_idx)
    result = wh_setting.get_requests(api=api)
    return result

def read(project_idx,shot_idx):
    api = api_list.shot_read %(project_idx,shot_idx)
    result = wh_setting.get_requests(api=api)
    return result

def create(project_idx,episode_idx,sequence_idx,shot_name,description="",status_idx="1"):
    api = api_list.shot_create %(project_idx,episode_idx,sequence_idx)
    data = {"shot_name":shot_name,"description":description,"status_idx":status_idx}
    result = wh_setting.post_requests(api=api, data=data)
    return result


def thumbnail_update(project_idx,shot_idx,thumbnail_path):
    api = api_list.shot_thumbnail_up %(project_idx,shot_idx)
    thumbnail = open(thumbnail_path,'rb')
    data = {"attached":thumbnail}
    result = wh_setting.post_requests(api=api, files=data)
    return result


def overview(project_idx,episode_idx=""):
    if episode_idx == "":
        api = api_list.shot_overview_all %(project_idx)
    else :
        api = api_list.shot_overview %(project_idx,episode_idx)
    result = wh_setting.get_requests(api=api)
    return result

def relation(project_idx,episode_idx):
    api = api_list.shot_relation %(project_idx,episode_idx)
    result = wh_setting.get_requests(api=api)
    return result['overview']