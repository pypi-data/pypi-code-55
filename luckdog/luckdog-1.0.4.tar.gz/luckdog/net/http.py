# -*- coding: utf-8 -*-

import requests
import json

class HEADER(object):
    __headers = {}

    def init(self, header):
        if not self.__headers:
            self.__headers = header
        return self

    def add(self, key, val):
        self.__headers[key] = val
        return self.__value()

    def delete(self, name):
        self.__headers.pop(name)
        return self.__value()

    def clear(self):
        self.__headers = None
        return self.__value()

    def __value(self):
        return self.to_string(self.__headers)
     
    def to_string(self, json_dict):
        return json.dumps(json_dict)

    def update(self, json):
        for key, val in json:
            self.__headers[key]=val
        return self.__value()

    def get_headers(self):
        return self.__headers
    pass

class COOKIES(object):
    """ 初始化 key_vals_str """
    """ 维护 key_vals_json """
    """ 呈现使用 key_vals_str """

    key_vals_str=None
    key_vals_json={}

    def length(self):
        return len(self.key_vals_json)

    def init(self, cookie):
        if not self.key_vals_str:
            self.key_vals_str = cookie
        self.key_vals_json = self.to_json(self.key_vals_str)
        self.__value()
        return self

    def add(self, key, val):
        key = key.strip()
        self.key_vals_json[key]=val
        return self.__value()

    def delete(self, name):
        self.key_vals_json.pop(name)
        return self.__value()

    def clear(self):
        self.key_vals_json = None
        return self.__value()

    def __value(self):
        self.key_vals_str = self.to_string(self.key_vals_json)
        return self.key_vals_str
     
    def to_string(self, key_vals_json_tmp):
        tmp_string = ""
        if not json:
            return tmp_string
        for key, val in key_vals_json_tmp.items():
            tmp_string = tmp_string + key + "=" + val +";"
        return tmp_string

    def to_json(self, key_vals_str_tmp):
        key_vals_json_tmp={}
        key_val_list = key_vals_str_tmp.split(";")
        for key_val in key_val_list:
            co_list = key_val.split("=")
            if len(co_list) >1:
                key_tmp = co_list[0].strip()
                val_tmp = co_list[1].strip()
                if key_tmp: 
                    key_vals_json_tmp[key_tmp]=val_tmp
            elif len(co_list) >0:
                key_tmp = co_list[0].strip()
                if key_tmp: 
                    key_vals_json_tmp[key_tmp]=""
        return key_vals_json_tmp

    def update_json(self, key_vals_json_new):
        for key, val in key_vals_json_new:
            key = key.strip()
            self.key_vals_json[key]=val
        return self.__value()

    def update_str(self, key_vals_str_new):
        key_vals_json_new_tmp = self.to_json(key_vals_str_new)
        for key, val in key_vals_json_new_tmp.items():
            self.key_vals_json[key]=val
        return self.__value()

    def cookie(self):
        return self.__value()

    def cookie_show_json(self):
        return self.to_json(self.key_vals_str)

class WBrowser(object):
 
    __url = ""
    __data = None  # post请求数据类型， 
    __json = None  # post请求json类型， 输入类型dict
    __headers_dict = None  # 类型字典 dict
    __method = 'get'
    __params = None # url后面的参数, 

    __response = None

    def __init__(self,headers=None):
        self.__headers_dict = headers
        pass

    def url(self, url):
        self.__url = url
        return self

    def method(self, method):
        self.__method = method
        return self

    def header(self, header_dict):
        self.__headers_dict = header_dict
        return self

    def get_header(self):
        return self.__headers_dict

    def body_json(self, json):
        self.__json = json
        return self

    def __visit(self):
        method_name = self.__method.lower()
        # 注意request的 **kwargs可用于扩展
        if('get' == method_name):

            response = requests.get(self.__url, params=self.__params, headers=self.__headers_dict)
            pass

        if('post' == method_name):
            # 
            print(self.__method, self.__url,  self.__data,  self.__json )
            
            response = requests.post(self.__url, 
            data=self.__data, 
            json=self.__json, 
            headers=self.__headers_dict)
            pass
        self.__response = response
        return self.__response

    def visit(self):
        """
        :: request
        request.post(url, data=None, json=None, file=None, **kwargs):
        request.get(url, params=None, **kwargs):

        :: response
        response.status_code
        response.text
        response.encoding
        response.apparent_encoding
        response.content
        response.headers
        """

        return self.__visit()
    pass

browser = WBrowser()
