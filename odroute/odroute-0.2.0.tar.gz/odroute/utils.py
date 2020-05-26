# -*- coding: utf-8 -*-

def index_by_dict_key(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def index_by_obj_prop(list, prop, value):
    for i, obj in enumerate(list):
        if getattr(obj, prop) == value:
            return i
    return -1


