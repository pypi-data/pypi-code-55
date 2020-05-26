# -*- coding: utf-8 -*-
from urllib3._collections import HTTPHeaderDict

from . import wh_setting, api_list



def key(task_idx, which='shot or asset'):
    api = api_list.publish_key %(which,task_idx)
    result = wh_setting.post_requests(api=api)
    return result['publish_key']

def key_read(publish_key):
    api = api_list.publish_key_read
    data = {'publish_key':publish_key}
    result = wh_setting.post_requests(api=api,data=data)
    return result

def create(task_idx='',
           which='shot or asset',
           version_idx='',
           publish_name ='',
           task_status_idx='',
           version_status_idx='',
           publish_path=[],
           description='',
           tag=''):

    #api 세팅
    api = api_list.publish_create %(which)

    #기본 데이터 세팅
    publish_key = key(task_idx,which)
    key_data = key_read(publish_key)


    #publish_path 파일 폴더 체크
    publish_path_check = wh_setting.file_folder_check(publish_path)
    if publish_path_check == None:
        print("등록 가능한 Path가 없어, 퍼블리시를 등록 할 수 없습니다.")
        return "error"

    else:
        main_path = (publish_path_check['file']+publish_path_check['folder'])[0]
        data = {"which":which,
                "version_idx":version_idx,
                "description": description,
                "publish_key":publish_key,
                "project_idx":key_data['project_idx'],
                "publish_name":publish_name,
                "main_path":main_path,
                "attached_path[]": publish_path_check['file'],
                "attached[]":publish_path_check['file'],
                "attached_folder[]":publish_path_check['folder'],
                "task_status_idx":task_status_idx,
                "version_status_idx":version_status_idx,
                "tag":tag
                }


        if which =="shot" :
            shot_data={"episode_idx": key_data['episode_idx'],
                       "sequence_idx": key_data['sequence_idx'],
                       "shot_idx": key_data['shot_idx']}
            data.update(shot_data)

        elif which =="asset":
            asset_data={"asset_category_idx": key_data['asset_category_idx'],
                        "asset_idx": key_data['asset_idx']}
            data.update(asset_data)
        else:
            print("which error")

        print("main_path:",main_path)

        result = wh_setting.post_requests(api=api, data=data)
        return result