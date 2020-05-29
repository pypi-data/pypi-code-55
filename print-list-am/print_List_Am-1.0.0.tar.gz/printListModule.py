#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:10:29 2020

@author: ignitarium
"""

# recursive printing function
def recursive_print_list(lst):
    for item in lst:
        if(isinstance(item, list)):
            recursive_print_list(item)
        else:
            print(item)