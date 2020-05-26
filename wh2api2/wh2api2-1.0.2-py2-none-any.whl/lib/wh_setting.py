# -*- coding: utf-8 -*-
import requests, json, os


from .. import wh


def get_requests (api,data="",observed_user_idx=''):
    #observed_user_idx는 myTask의 observe 기능 사용시

    #쿠키세팅
    cookies = wh.Login.whtoken.copy()
    if observed_user_idx != "":
        if type(observed_user_idx) == int:
            observed_user_idx = str(observed_user_idx)

        cookies["observed_user_idx"] = observed_user_idx

    request_result = requests.get(wh.Login.url+api, data=data, cookies=cookies)
    json_list = result(request_result)
    return json_list

def post_requests (api,data="",files=""):
    request_result = requests.post(wh.Login.url+api, files=files,data=data, cookies=wh.Login.whtoken)
    json_list = result(request_result)
    return json_list


# 결과 확인
def result(result):

    if result.status_code == 200:
        json_list = json.loads(result.text)['data']
        print(json.loads(result.text)['error']['message'])
        return json_list
    else:
        errorcode = "errorcode:"+str(result.status_code)
        print(errorcode)
        return result

def file_folder_check(path_list):
    file_list = []
    folder_list=[]
    for path in path_list:
        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            folder_list.append(path)
        else:
            print('확인 불가능: ',path)

    if file_list ==[] and folder_list == []:
        return None
    else:
        return {"file":file_list,"folder":folder_list}
