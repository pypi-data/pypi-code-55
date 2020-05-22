# -*- coding: utf-8 -*-
"""
Created on Fri May 22 14:22:31 2020

@author: huzhen
"""
import time


class Today:
    def __init__(self):
        pass
    def today(self):
        _ = time.gmtime()
        _ = list(_)[:3]
        return str(_[0]) + '年' + str(_[1]) + '月' + str(_[2]) + '日'
    