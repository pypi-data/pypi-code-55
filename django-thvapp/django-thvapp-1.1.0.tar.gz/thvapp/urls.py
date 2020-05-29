#!/usr/bin/env python
# encoding: utf-8
# @author: Tianyang
# @license: (C) Copyright 2013-2020/4/20, NSCC-TJ.AllRightsReserved.
# @contact: tianyang@nscc-tj.cn
# @software: 
# @file: urls.py
# @time: 2020/4/20 18:43
# @desc:

from django.urls import path
import thvapp.views as thvapps

urlpatterns = [
    path('thva/apps', thvapps.visualApps),
    path('open/app', thvapps.openApp),
    path('close/app',thvapps.closeApp),
    path('list/app', thvapps.listApp),
]