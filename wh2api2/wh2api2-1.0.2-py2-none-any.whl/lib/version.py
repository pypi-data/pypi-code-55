# -*- coding: utf-8 -*-

from . import wh_setting, api_list


def key(task_idx, which='shot or asset'):
    api = api_list.version_key %(which,task_idx)
    result = wh_setting.post_requests(api=api)
    return result['version_key']

def key_read(version_key):
    api = api_list.version_key_read
    data = {'version_key':version_key}
    result = wh_setting.post_requests(api=api,data=data)
    return result

def create(task_idx='',
           which='shot or asset',
           version_name='',
           task_status_idx='',
           version_status_idx='',
           reviewer_user_idx='',
           hour_spent='',
           version_path=[],
           metadata= [],
           description="",
           cc_user_idx='',
           thumbnail_path = ""):


#기본값 세팅
    version_key = key(task_idx,which)
    key_data = key_read(version_key)

#api 세팅
    api = api_list.version_create %(which)

#파일 유효성 검사
    version_path_check = wh_setting.file_folder_check(version_path)
    if version_path_check == None or version_path_check['file'] == []:
        print("업로드할 파일이 없습니다.")
        return 'error'

    else:
        data = {"which":which,
                "description": description,
                "version_key":version_key,
                "project_idx":key_data['project_idx'],
                "version_name":version_name,
                "task_status_idx":task_status_idx,
                "version_status_idx":version_status_idx,
                "hour_spent":hour_spent,
                "reviewer_user_idx":reviewer_user_idx,
                "main_path":version_path_check['file'][0],
                "attached_path[]":version_path_check['file'],
                "cc_user_idx[]":cc_user_idx,
                "metadata[]":metadata,
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


    #file 데이터 정리

        files = []
        for version in version_path_check['file']:
            version_file = ('attached[]',open(version,'rb'))
            files.append(version_file)

        if thumbnail_path != "":
            thumbnail_open = open(thumbnail_path, 'rb')
            thumbnail_data = ("thumbnail",thumbnail_open)
            files.append(thumbnail_data)

        print(version_path_check['file'][0],version_path_check['file'],files)
        result = wh_setting.post_requests(api=api, data=data,files=files)
        return result