# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def read(org_id="std"):
    api = api_list.org_read %(org_id)
    result = wh_setting.get_requests(api=api)
    return result