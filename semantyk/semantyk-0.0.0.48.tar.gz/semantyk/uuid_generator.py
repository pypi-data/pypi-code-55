# -*- coding: utf-8 -*-
##################################################
#
# uuid_generator
# Module | UUID Generator
#
# Daniel Bakas Amuchastegui
# March 16, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
##################################################

import uuid

def generate_uuid():
    letters = {'a','b','c','d','e','f'}
    result = '0'
    while result[0] not in letters:
        result = uuid.uuid4().hex
        result = result[0:8] + '_' + result[8:12] + '_' + result[12:16] + '_' + result[16:20] + '_' + result[20:]
    return result