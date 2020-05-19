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


class Fooo(object):
    def __init__(self):
        print 'fooo init'

    def entry_point(self):
        print "entry_point" * 100


if __name__ == '__main__':
    f = Fooo()
    f.entry_point()




