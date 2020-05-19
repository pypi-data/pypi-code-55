# -*- coding: utf-8 -*-

import json
import re

class UtilJson(object):
    "container->ip@[0]"
    "container->ip@[1]->tel@[1]"
    "container->ip@[1]"
    "container->ip@[*]"

    "data->machines@[0]->ip@[$(cluster=hz)]"
    

    num =0
    # TODO delete 
    def get_element_by_key(self, key, src_dict):
        """ return list element, or a element """
        if isinstance(src_dict, list):
            list_key = key.split("@")
            if len(list_key) < 2:
                raise  DogException("src_dict is list, but key used a error type,just ip@[1] is supported.")
            elif len(list_key) == 2:
                index = list_key[1][1:-1]
                """
                @[*]
                @[0]
                @[1]
                @[$(cluster=hz)]
                
                """
                # print(index)
                if index == "*" :
                    element_list = []
                    for element in src_dict:
                        element_list.append(self.__element(list_key[0],element))
                    return element_list
                else :
                    fit_index = re.search(r'^\[[0-9]+\]$', list_key[1])
                    if fit_index  :
                        # print("fit_index finded", list_key[1])
                        # TODO index may big then len(src_dict)
                        return self.__element(list_key[0],src_dict[int(index)])
                    
                    fit_attribute = re.search('^\[\$\(.*?\)\]$', list_key[1])
                    if fit_attribute:
                        element_list = []
                        attr = index[2:-1]
                        # print("fit_attribute", attr)
                        attr_name_val = attr.split("=")
                        for element in src_dict:
                            # print(self.__element(attr_name_val[0],element))
                            # print("".join(attr_name_val[1:]))
                            if self.__element(attr_name_val[0],element) == "".join(attr_name_val[1:]):
                                element_list.append(self.__element(list_key[0],element))
                        return element_list
        else:
            # print("<<< ",key)
            return self.__element(key,src_dict)
        # print("____________________________________________________________")
        return None

    def __element(self, key, src_dict):
        element = None
        # if not src_dict:
        #     raise Exception("'NoneType' object has no attribute 'keys'")
        if key in src_dict.keys():
            element = src_dict[key]
            pass
        # print(">>> ", key," __ ", src_dict)
        # print(type(src_dict))
        
        # print(element)
        return element
    # TODO delete 
    def get_element_by_keypath(self, keypath, src_dict):
        # print("get_element_by_keypath", keypath, src_dict)
        # print(keypath)
        keypath_list = keypath.split("->")
        # print(len(keypath_list))
        if len(keypath_list)>1:
            first_key = keypath_list[0]
            sub_keypath = "->".join(keypath_list[1:])
            sub_src_dict = self.get_element_by_key(first_key, src_dict)

            # if isinstance(sub_src_dict, list):
            #     for element in sub_src_dict:
            #         return self.get_element_by_keypath(sub_keypath,element)
            #         pass
            #     pass
            return self.get_element_by_keypath(sub_keypath,sub_src_dict)

        elif len(keypath_list)>0:
            first_keypath = keypath_list[0]
            # print(first_keypath)
            sub_element_or_list = self.get_element_by_key(first_keypath, src_dict)
            return sub_element_or_list
        else:
            raise DogException("get_element_by_keypath： keypath exception.")


    def find_elements_by_key(self, key, src_dict_list):
            list_key = key.split("@")
            if len(list_key) < 2:
                raise  DogException("src_dict is list, but key used a error type,just ip@[1] is supported.")
            elif len(list_key) == 2:
                index = list_key[1][1:-1]
                """
                @[*]
                @[0]
                @[1]
                @[$(cluster=hz)]
                
                """
                # print(index)
                if index == "*" :
                    element_list = []
                    for element in src_dict_list:
                        element_list.append(self.__element(list_key[0],element))
                    return element_list
                else :
                    fit_index = re.search(r'^\[[0-9]+\]$', list_key[1])
                    # print("TODO find","fit_index", list_key[1])
                    if fit_index  :
                        # print("fit_index finded", list_key[1])
                        # TODO index may big then len(src_dict)
                        return self.__element(list_key[0],src_dict_list[int(index)])
                    
                    fit_attribute = re.search('^\[\$\(.*?\)\]$', list_key[1])
                    if fit_attribute:
                        element_list = []
                        attr = index[2:-1]
                        # print("fit_attribute", attr)
                        attr_name_val = attr.split("=")
                        for element in src_dict_list:
                            # print(self.__element(attr_name_val[0],element))
                            # print("".join(attr_name_val[1:]))
                            if self.__element(attr_name_val[0],element) == "".join(attr_name_val[1:]):
                                element_list.append(self.__element(list_key[0],element))
                        return element_list
    
    def find_element_by_keypath(self, keypath, src_dict):
        keypath_list = keypath.split("->")
        first_key = keypath_list[0]
        if isinstance(src_dict, list):
            sub_src_dict_element_list = self.find_elements_by_key(first_key, src_dict)
            if not sub_src_dict_element_list  or  sub_src_dict_element_list == "null" :
                return sub_src_dict_element_list
            if len(keypath_list)>1:
                sub_keypath = "->".join(keypath_list[1:])
                res_list = []
                for sub_src_dict_element in sub_src_dict_element_list:
                    if not sub_src_dict_element:
                        element = None
                    else:
                        element = self.find_element_by_keypath(sub_keypath, sub_src_dict_element) 
                        res_list.append(element) 
                return res_list
            else:
                return sub_src_dict_element_list
        else:
            sub_src_dict_element = self.__element(first_key, src_dict) 
            if not sub_src_dict_element or  sub_src_dict_element == "null" :
                return sub_src_dict_element
            if len(keypath_list)>1:
                sub_keypath = "->".join(keypath_list[1:])
                return self.find_element_by_keypath(sub_keypath,sub_src_dict_element) 
            else:
                return sub_src_dict_element

    def json_loads(self, src_json_str):
        return json.loads(src_json_str)

    def json_dumps(self, src_json_dict):
        return json.dumps(src_json_dict)

    def json_pretty_printed(self, src_json_dict):
        src_json_dict_tmp = src_json_dict
        if isinstance(src_json_dict, str) :
            src_json_dict_tmp = self.json_loads(src_json_dict)
        return json.dumps(src_json_dict_tmp ,sort_keys=True, indent=4,ensure_ascii=False)

    def json_compress_str(self, src_json_dict):
        return json.dumps(src_json_dict)
    pass





class DogException(Exception):

    pass

util_json = UtilJson()

# src_dict_str="{\"id\":894,\"package\":{\"id\":117,\"name\":\"docker.cloud.new.0.5-2(微应用大内存)\",\"cpu\":\"0.5\",\"cpu_extend_max\":\"2\",\"memory\":\"6144Mi\",\"memory_extend_max\":\"6144Mi\",\"network\":\"1\"},\"container\":[{\"id\":786066,\"package\":{\"id\":117,\"name\":\"docker.cloud.new.0.5-2(微应用大内存)\",\"cpu\":\"0.5\",\"cpu_extend_max\":\"2\",\"memory\":\"6144Mi\",\"memory_extend_max\":\"6144Mi\",\"network\":\"1\"},\"location\":{\"id\":1,\"name\":\"阿里云-华东一区\"},\"key\":786066,\"tag_fmt\":[],\"name\":\"mall-hz-565f5c67bb-h6j42\",\"instance_id\":null,\"ip\":\"172.22.34.146\",\"host_ip\":\"10.111.11.127\",\"node\":\"\",\"pip\":null,\"cpu\":0,\"memory\":0,\"disk\":0,\"zone\":\"cn-hangzhou-h\",\"status\":\"Running\",\"description\":null,\"category\":\"cloud-docker\",\"docker_flag\":0,\"cost\":0.01,\"resource_version\":0,\"restart_count\":0,\"ready\":true,\"image\":\"harbor.ymmoa.com/app/mall:war-master-jdk8-20200311_163914\",\"reason\":\"\",\"lane\":\"default\",\"share\":0,\"age\":\"25天49分\",\"channel_sign\":\"\",\"create_time\":\"2020-03-26T13:06:03Z\",\"expires_time\":null,\"jmap_status\":null,\"jmap_package_url\":null,\"tag\":[]},{\"id\":789292,\"package\":{\"id\":117,\"name\":\"docker.cloud.new.0.5-2(微应用大内存)\",\"cpu\":\"0.5\",\"cpu_extend_max\":\"2\",\"memory\":\"6144Mi\",\"memory_extend_max\":\"6144Mi\",\"network\":\"1\"},\"location\":{\"id\":1,\"name\":\"阿里云-华东一区\"},\"key\":789292,\"tag_fmt\":[],\"name\":\"mall-hz-565f5c67bb-7gqdz\",\"instance_id\":null,\"ip\":\"172.22.16.80\",\"host_ip\":\"10.111.11.89\",\"node\":\"\",\"pip\":null,\"cpu\":0,\"memory\":0,\"disk\":0,\"zone\":\"cn-hangzhou-h\",\"status\":\"Running\",\"description\":null,\"category\":\"cloud-docker\",\"docker_flag\":0,\"cost\":0.01,\"resource_version\":0,\"restart_count\":0,\"ready\":true,\"image\":\"harbor.ymmoa.com/app/mall:war-master-jdk8-20200311_163914\",\"reason\":\"\",\"lane\":\"default\",\"share\":0,\"age\":\"24天2时17分\",\"channel_sign\":\"\",\"create_time\":\"2020-03-27T11:38:46Z\",\"expires_time\":null,\"jmap_status\":null,\"jmap_package_url\":null,\"tag\":[]},{\"id\":851008,\"package\":{\"id\":117,\"name\":\"docker.cloud.new.0.5-2(微应用大内存)\",\"cpu\":\"0.5\",\"cpu_extend_max\":\"2\",\"memory\":\"6144Mi\",\"memory_extend_max\":\"6144Mi\",\"network\":\"1\"},\"location\":{\"id\":1,\"name\":\"阿里云-华东一区\"},\"key\":851008,\"tag_fmt\":[],\"name\":\"mall-gpre-7b877857b9-26b28\",\"instance_id\":null,\"ip\":\"172.22.123.79\",\"host_ip\":\"10.111.11.7\",\"node\":\"\",\"pip\":null,\"cpu\":0,\"memory\":0,\"disk\":0,\"zone\":\"cn-hangzhou-h\",\"status\":\"Running\",\"description\":null,\"category\":\"cloud-docker\",\"docker_flag\":0,\"cost\":0.01,\"resource_version\":0,\"restart_count\":0,\"ready\":true,\"image\":\"harbor.ymmoa.com/app/mall:war-master-jdk8-20200420_173025\",\"reason\":\"\",\"lane\":\"default\",\"share\":0,\"age\":\"2时59分\",\"channel_sign\":\"gpre\",\"create_time\":\"2020-04-20T10:56:40Z\",\"expires_time\":null,\"jmap_status\":null,\"jmap_package_url\":null,\"tag\":[]},{\"id\":851009,\"package\":{\"id\":117,\"name\":\"docker.cloud.new.0.5-2(微应用大内存)\",\"cpu\":\"0.5\",\"cpu_extend_max\":\"2\",\"memory\":\"6144Mi\",\"memory_extend_max\":\"6144Mi\",\"network\":\"1\"},\"location\":{\"id\":1,\"name\":\"阿里云-华东一区\"},\"key\":851009,\"tag_fmt\":[],\"name\":\"mall-gpre-7b877857b9-9wj8f\",\"instance_id\":null,\"ip\":\"172.22.6.190\",\"host_ip\":\"10.111.11.130\",\"node\":\"\",\"pip\":null,\"cpu\":0,\"memory\":0,\"disk\":0,\"zone\":\"cn-hangzhou-h\",\"status\":\"Running\",\"description\":null,\"category\":\"cloud-docker\",\"docker_flag\":0,\"cost\":0.01,\"resource_version\":0,\"restart_count\":0,\"ready\":true,\"image\":\"harbor.ymmoa.com/app/mall:war-master-jdk8-20200420_173025\",\"reason\":\"\",\"lane\":\"default\",\"share\":0,\"age\":\"2时43分\",\"channel_sign\":\"gpre\",\"create_time\":\"2020-04-20T11:12:33Z\",\"expires_time\":null,\"jmap_status\":null,\"jmap_package_url\":null,\"tag\":[]}],\"yaml\":[],\"auto\":{\"id\":264,\"min_replicas\":2,\"max_replicas\":4,\"target_cpu_percentage\":100,\"current_replicas\":2,\"current_cpu_percentage\":300,\"user\":\"10304\",\"username\":\"李波\",\"ctime\":\"2018-11-21T03:56:58.350657Z\",\"utime\":\"2019-06-17T09:48:57.105017Z\"},\"deployment\":\"mall-hz\",\"project_name\":\"mall\",\"generate_name\":\"mall-hz-7c9d588c84-9wsw8\",\"namespace\":\"prod\",\"lane\":\"default\",\"env\":\"hz\",\"full_path\":\"com.ymm.bop.mall.mall-app.hz\",\"replicas\":2,\"description\":null,\"user\":\"9999\",\"username\":\"张小伟\",\"status\":\"running\",\"unavailableReplicas\":0,\"label\":\"\",\"ctime\":\"2018-09-26T09:21:03.777588Z\",\"utime\":\"2020-04-16T13:56:02.828817Z\"}"
# src_dict=json.loads(src_dict_str)
# util_json = UtilJson()
# keypath="container->ip@[0]"
# dist = util_json.get_element_by_keypath(keypath, src_dict)
# print(dist)




