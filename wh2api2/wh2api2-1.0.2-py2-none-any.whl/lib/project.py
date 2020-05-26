# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(finished=""):
    # finished = '1' 끝난 프로젝트도 조회
    api = api_list.project_list
    data = {"including_finished": finished, "all": "1"}
    result = wh_setting.get_requests(api=api,data=data)
    return result

def read(project_idx):
    api = api_list.project_read %(project_idx)
    result = wh_setting.get_requests(api=api)
    return result