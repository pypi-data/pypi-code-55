# -*- coding: utf-8 -*-

from . import wh_setting, api_list


def read(task_idx):
    api = api_list.shot_task_read %(task_idx)
    result = wh_setting.get_requests(api=api)
    return result

def list(project_idx,shot_idx):
    api = api_list.shot_task_list %(project_idx,shot_idx)
    result = wh_setting.get_requests(api=api)
    return result

def create(project_idx,shot_idx,tasktype_name):
    api = api_list.shot_task_create %(project_idx,shot_idx)
    data = {"tasktype_name":tasktype_name}
    result = wh_setting.post_requests(api=api,data=data)
    return result

def status_change(project_idx,task_idx,status_idx):
    api = api_list.shot_task_status_change %(project_idx,task_idx)
    data = {"status_idx":status_idx}
    result = wh_setting.post_requests(api=api,data=data)
    return result

def start(project_idx,task_idx):
    api = api_list.shot_task_start %(project_idx,task_idx)
    result = wh_setting.post_requests(api=api)
    return result

def stop(project_idx,task_idx):
    api = api_list.shot_task_stop %(project_idx,task_idx)
    result = wh_setting.post_requests(api=api)
    return result
