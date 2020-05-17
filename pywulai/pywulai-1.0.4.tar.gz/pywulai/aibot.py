import time
import json
import hashlib
import string
import random
import requests
import pyrda.sqlserver as sqlserver
import pyrdo.list as rdlist
# 定义函数
def GetChars(length):
    CHAR_LIST = []
    [[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
    [[CHAR_LIST.append(e) for e in string.ascii_letters] for i in range(0, 2)]
    [[CHAR_LIST.append(e) for e in string.digits] for i in range(0, 2)]
    random.shuffle(CHAR_LIST)
    return "".join(CHAR_LIST[0:length])
#  添加头部认证文件
#  同时有相应的写入文件
def get_headers(pubkey:dict(type=str,help="the pubKey for wulai app"), secret:dict(type=str,help="the secret for wulai app")):
    timestamp = str(int(time.time()))
    nonce = GetChars(32)
    upwd = nonce + timestamp + secret
    s1 = hashlib.sha1()
    s1.update(upwd.encode("utf-8"))
    sign = s1.hexdigest()
    #    sign = hashlib.sha1(nonce + timestamp + secret).hexdigest()
    data = {
        "pubkey": pubkey,
        "sign": sign,
        "nonce": nonce,
        "timestamp": timestamp
    }
    headers = {}
    for k, v in data.items():
        headers["Api-Auth-" + k] = v
    return headers
def get_headers_km(conn,app_id):
    sql = "select Fpubkey,Fsecret from t_km_app where Fapp_id='%s' and Fstatus = 1" % app_id
    data = sqlserver.sql_select(conn,sql)
    pubkey = data[0][0]
    secret = data[0][1]
    return get_headers(pubkey,secret)
# 定义简化版的提交
# headers get from get_headers()
def rd_post(headers, api, data):
    return requests.post(url=api, json=data, headers=headers)
# 创建用户
def laiye_user_create(headers, user_name="test", user_id="123-123"):
    #headers = get_headers()
    api = "https://openapi.wul.ai/v2/user/create"
    data = {"nickname": user_name,
            "avatar_url": "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=4090426978,2527772527&fm=15&gp=0.jpg",
            "user_id": user_id}
    r = rd_post(headers,api,data)
    res = len(r.json())
    if res == 0:
        return user_id
    else:
        return "error"
# 创建用户
def user_create(headers,user_name="test", user_id="123-123"):
    # print(laiye_user_create(headers=headers,user_name=user_name,user_id=user_id))
    return laiye_user_create(headers=headers,user_name=user_name,user_id=user_id)
# 查询用户
def user_query(headers, user_id='126', format='list'):
    api = "https://openapi.wul.ai/v2/user/get"
    data = {
        "user_id": user_id
    }
    r = rd_post(headers=headers, api=api, data=data)
    if format == 'list':
        res = rdlist.dict_values_list(r.json())
    else:
        res = r.json()
    return res
def laiye_decode(data, format='list'):
    # msg_id = data['msg_id']
    msg_body = data["suggested_response"]
    res = []
    if format == 'list':
        for i in range(len(msg_body)):
            item = []
            data_entry = msg_body[i]
            res_txt = data_entry['response'][0]["msg_body"]["text"]["content"]
            res_score = data_entry['score']
            res_send = data_entry['is_send']
            res_ques_std = data_entry['bot']['qa']['standard_question']
            res_ques_sys = data_entry['bot']['qa']['question']

            item.append(res_ques_std)
            item.append(res_score)
            item.append(res_ques_sys)
            item.append(res_txt)

            # item.append(res_send)
            # item.append(i+1)
            res.append(item)
    else:
        for i in range(len(msg_body)):
            item = {}
            data_entry = msg_body[i]
            res_txt = data_entry['response'][0]["msg_body"]["text"]["content"]
            res_score = data_entry['score']
            res_send = data_entry['is_send']
            res_ques_std = data_entry['bot']['qa']['standard_question']
            res_ques_sys = data_entry['bot']['qa']['question']

            item['ques_std'] = res_ques_std
            item['score'] = res_score
            item['ques_match'] = res_ques_sys
            item['answer'] = res_txt

            # item.append(res_send)
            # item.append(i+1)
            res.append(item)

    return res


def laiye_bot(headers, query_text, user_id='126', format='list'):
    data = {
        "msg_body": {
            "text": {
                "content": query_text
            }
        },
        "user_id": user_id,
        "extra": "string"
    }
    api = 'https://openapi.wul.ai/v2/msg/bot-response'
    res_get = rd_post(headers,api,data)
    print(res_get.json())
    return (laiye_decode(res_get.json(), format))


def aibot_query(headers, query_text, user_id='126', format='list'):
    return laiye_bot(headers, query_text, user_id, format)

if __name__ == "__main__":
    conn = sqlserver.conn_create('115.159.201.178','sa','Hoolilay889@','rdbe')
    headers = get_headers_km(conn,'caas')
    res3 = user_create(headers=headers, user_name='test5', user_id='127')
    print(res3)
    #查询用户
    user1 = user_query(headers=get_headers_km(conn,'caas'), user_id='127',format='lists')
    print(user1)
    kmtest = aibot_query(headers=get_headers_km(conn,'caas'),query_text='发现运行版多少钱', user_id='127', format='list')
    print(kmtest)
