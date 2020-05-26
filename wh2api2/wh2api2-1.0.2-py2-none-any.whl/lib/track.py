# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def version(project_idx,from_date="yyyy-mm-dd",to_date="yyyy-mm-dd",last=""):
    #last = "" or "last"
    api = api_list.track_version %(project_idx,from_date,to_date,last)
    result = wh_setting.get_requests(api=api)
    return result