#!/usr/bin/env python
# encoding: utf-8
# @author: Tianyang
# @license: (C) Copyright 2013-2020/1/3, NSCC-TJ.AllRightsReserved.
# @contact: tianyang@nscc-tj.cn
# @software: 
# @file: admin.py
# @time: 2020/1/3 11:05
# @desc:

from django.contrib import admin
# Register your models here.

from thStorage.models import NetDiskUser
admin.site.register(NetDiskUser)