# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(project_idx,episode_idx):
    api = api_list.sequence_list %(project_idx,episode_idx)
    result = wh_setting.get_requests(api=api)
    return result

def create(project_idx,episode_idx,sequence_name,description=""):
    api = api_list.sequence_create %(project_idx,episode_idx)
    data = {"sequence_name":sequence_name,"description":description}
    result = wh_setting.post_requests(api=api,data=data)
    return result