#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/25 17:05
# @Author : yangpingyan@gmail.com
import os, sys, inspect

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
exec_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DEBUG_MODE = False
if 'pytool' not in exec_path:
    exec_path = os.path.join(exec_path, 'pytool')
    DEBUG_MODE = True

if __name__ == '__main__':
    print("Mission start!")

    print("Mission complete!")
    