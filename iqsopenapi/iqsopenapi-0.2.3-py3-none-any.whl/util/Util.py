# -*- coding: utf-8 -*-
import time
import sys
import os
import json
import datetime

def ExecutedTime(func):
    start = time.time()
    result = func()
    end = time.time()
    escape = end - start
    return escape, result

def Minimum(values, func):
    value = None
    last = None
    for x in values:
        result = func(x)
        if not last or last > result:
            value = x
            last = result
    return value

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)