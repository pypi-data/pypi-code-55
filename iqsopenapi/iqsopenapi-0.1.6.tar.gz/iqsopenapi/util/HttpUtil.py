# -*- coding: utf-8 -*-
import urllib.request
import ssl
import json

def httpGet(url):
    '''GET请求'''
    ssl._create_default_https_context = ssl._create_unverified_context
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    res_data = urllib.request.urlopen(request,timeout=30)
    res = res_data.read().decode("utf-8")
    return res

def httpJsonPost(reqUrl,dict):
    '''POST请求 application/json'''
    ssl._create_default_https_context = ssl._create_unverified_context   
    data = json.dumps(dict) 
    data = bytes(data,'utf8') 
    request = urllib.request.Request(url = reqUrl,data = data)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    request.add_header('Content-Type', 'application/json')
    res_data = urllib.request.urlopen(request,timeout=30)
    res = res_data.read().decode("utf-8")
    return res

def httpFormPost(reqUrl,params):
    '''POST请求 application/json'''
    ssl._create_default_https_context = ssl._create_unverified_context   
    data = bytes(params,'utf8') 
    request = urllib.request.Request(url = reqUrl,data = data)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    res_data = urllib.request.urlopen(request,timeout=30)
    res = res_data.read().decode("utf-8")
    return res

def httpPost(reqUrl,dict):
    '''POST请求'''
    ssl._create_default_https_context = ssl._create_unverified_context   
    data = urllib.parse.urlencode(dict).encode('utf-8')
    request = urllib.request.Request(url = reqUrl,data = data)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
    res_data = urllib.request.urlopen(request,timeout=30)
    res = res_data.read().decode("utf-8")
    return res

if __name__ == '__main__':    
    resp = httpGet('https://stgyapi.inquant.cn/future/Contract/Get?symbol=rb1905&exchange=4')
    print(resp)
