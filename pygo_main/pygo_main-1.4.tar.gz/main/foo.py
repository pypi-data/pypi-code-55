#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/5/18 4:13 PM"
    __mail__ = "mingliang.gao@163.com"
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python foo.py
# ------------------------------------------------------------

class Foo(object):
    def __init__(self):
        print 'foo init'

    def __new__(cls, *args, **kwargs):
        print 'foo new'

    def run(self):
        print 'foo-' * 100

if __name__ == '__main__':
    Foo().run()
