#!/usr/bin/env python
# coding: utf-8

# In[26]:


import urllib
from datetime import datetime
from urllib.request import urlopen
from hashlib import md5
from os import system
from time import time

g_str_bucket_directory="cameo_cache/default/"

def _get_md5_filename_gs_http(str_key):
    str_hash_filename=f"""{md5(str_key.encode(encoding="utf-8")).hexdigest()}.cache"""
    s=str_hash_filename
    str_gs=f"gs://{g_str_bucket_directory}{s[0]}/{s[1]}/{s[2]}/{s[3]}/{s[4]}/{s[5]}/{s}"
    str_gs_http=f"http://storage.googleapis.com/{g_str_bucket_directory}{s[0]}/{s[1]}/{s[2]}/{s[3]}/{s[4]}/{s[5]}/{s}"
    return str_hash_filename,str_gs,str_gs_http
    
def set_bucket(str_bucket_directory):
    g_str_bucket_directory=str_bucket_directory

def get_str_cache(str_key):
    try:
        str_filename,str_gs,str_gs_http=_get_md5_filename_gs_http(str_key)
        print(f"get_str_cache:{str_gs_http}")
        return urlopen(f"{str_gs_http}?no_http_cache={time()}").read().decode("utf-8")
    except Exception as e:
        return ""

def make_cache(str_key,str_cache_content):
    str_filename,str_gs,str_gs_http=_get_md5_filename_gs_http(str_key)
    str_local_filename=f"/home/bohachu/cameo_cache/data/{str_filename}"
    io=open(str_local_filename,"w"); io.write(str_cache_content); io.close()
    print(f"make_cache:{str_gs}")
    system(f'/usr/bin/gsutil mv {str_local_filename} {str_gs}')

def hi():
    print("20200518 9:42 🐻🥑帥!")    

if __name__=="__main__":
    hi()
    set_bucket("gs://cameo_cache/default/")
    print("key1:",get_str_cache("key1"))
    make_cache("key2","16種🐶 value22222 中文很多🐻")
    print("key2:",get_str_cache("key2"))


# In[21]:


import time
time.time()


# In[73]:


from urllib.request import urlopen
import urllib
from hashlib import md5
from time import time
from datetime import datetime
import subprocess
import os
from os import system

def get_cache(str_url_quote_safe,str_bucket):
    t=datetime.now #縮寫 t() 可印出現在時間
    print(f"{t()},001 "+str_url_quote_safe)
    str_url=urllib.parse.unquote(str_url_quote_safe)
    str_hash_filename=f"""{md5(str_url.encode(encoding="utf-8")).hexdigest()}.cache"""
    s=str_hash_filename
    str_gs_url=f"http://storage.googleapis.com/{str_bucket}/{s[0]}/{s[1]}/{s[2]}/{s[3]}/{s[4]}/{s[5]}/{s}"
    str_gs_path=f"gs://{str_bucket}/{s[0]}/{s[1]}/{s[2]}/{s[3]}/{s[4]}/{s[5]}/{s}"
    dic={}
    try:
        print(f"{t()},004 "+str_gs_url)
        return urlopen(str_gs_url).read()
    except Exception as e:
        print(f"{t()}, {str_gs_url}, {e}")
    
    str_write_file=f"/home/bohachu/cameo_cache/cache/{str_hash_filename}"
    with open(str_write_file,"wb") as io:
        try:
            if(str_url.count("/")<1):
                print(f"{t()},005 str_url.count("/")<1 {str_url}")
            str_prefix,str_param=str_url.rsplit('/', 1)
            str_query=f"{str_prefix}/{urllib.parse.quote(str_param)}"
            str_query=str_query.replace("%3F","?") #還原問號
            print(f"""{t()},006 str_query.replace("%3F","?")"""+str_query)
            byte_response=urlopen(str_query).read()
        except Exception as e:
            str_err=f"{t()},007 Exception as e, {str_url}, {e}"
            print(str_err)
            return str_err
        io.write(byte_response)
        
    str_command=f"/usr/bin/gsutil mv {str_write_file} {str_gs_path}"
    system(str_command)
    return byte_response

def test_case1():
    t=datetime.now()
    str_url="https://iotai-dev.cameo.tw/api/v2/iot/events?start_time=2020-04-01 00:00:00&end_time=2020-04-29 23:59:59&min_lat=22.43422&max_lat=22.89&min_lon=120.1393&max_lon=120.4398"
    byte_content=get_cache(urllib.parse.quote(str_url, safe=''),"cameo_cache")
    print(f"len(byte_content):{len(byte_content)}")
    print(f"{datetime.now()-t}")

def test_case2():
    t=datetime.now()
    str_url="https://cameo.tw/3/ai/landing.html"
    byte_content=get_cache(urllib.parse.quote(str_url, safe=''),"cameo_cache")
    print(f"len(str_content):{len(byte_content)}:{byte_content[0:200]}")
    print(f"{datetime.now()-t}")
    
def test_case3():
    t=datetime.now()
    str_url="https://iotai-dev.cameo.tw/api/v2/iot/events?start_time=2020-04-01 00:00:10&end_time=2020-04-29 23:59:59&min_lat=22.43422&max_lat=22.89&min_lon=120.1393&max_lon=120.4398"
    byte_content=get_cache(urllib.parse.quote(str_url, safe=''),"cameo_cache")
    print(f"len(byte_content):{len(byte_content)}, byte_content: {byte_content[0:300]}")
    print(f"{datetime.now()-t}")
    
def test_case4():
    t=datetime.now()
    str_url="http://cameo.tw"
    byte_content=get_cache(urllib.parse.quote(str_url, safe=''),"cameo_cache")
    print(f"len(byte_content):{len(byte_content)}, byte_content: {byte_content[0:300]}")
    print(f"{datetime.now()-t}")

def test_case5():
    t=datetime.now()
    q="https%3A%2F%2Fiotai-dev.cameo.tw%2Fapi%2Fv2%2Fiot%2Fevents%3Fstart_time%3D2020-04-02%2000%3A00%3A01%26end_time%3D2020-04-29%2023%3A59%3A59%26min_lat%3D22.43422%26max_lat%3D22.89%26min_lon%3D120.1393%26max_lon%3D120.4398"
    byte_content=get_cache(q,"cameo_cache")
    print(f"len(byte_content):{len(byte_content)}, byte_content: {byte_content[0:300]}")
    print(f"{datetime.now()-t}")
    
    
if __name__=="__main__":
    test_case1()
    test_case2()
    test_case3()
    test_case4()
    test_case5()
    please_use_chrome_browser_to_test="""http://cache.cameo.tw/str_url_quote_safe=https%3A%2F%2Fiotai-dev.cameo.tw%2Fapi%2Fv2%2Fiot%2Fevents%3Fstart_time%3D2020-04-17%2000%3A00%3A00%26end_time%3D2020-04-29%2023%3A59%3A59%26min_lat%3D22.43422%26max_lat%3D22.89%26min_lon%3D120.1393%26max_lon%3D120.4398"""
    pass

