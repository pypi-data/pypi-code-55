#!/usr/bin/env python
# -*- coding: utf-8 -*-

#                                                           
# Copyright (C)2017 SenseDeal AI, Inc. All Rights Reserved  
#                                                           

"""                                                   
File: test.py
Author: lzl
E-mail: zll@sensedeal.ai
Last modified: 2019/4/8
Description:                                              
"""
from text_etl import handle_text


def test_content():
    in_file = 'demo/demo_7.html'
    with open(in_file, 'r') as f:
        content = f.read()

    res = handle_text(content)
    print(res)


test_content()
