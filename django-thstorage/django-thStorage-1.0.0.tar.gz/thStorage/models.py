#!/usr/bin/env python
# encoding: utf-8
# @author: Tianyang
# @license: (C) Copyright 2013-2020/1/3, NSCC-TJ.AllRightsReserved.
# @contact: tianyang@nscc-tj.cn
# @software: 
# @file: models.py
# @time: 2020/1/3 11:04
# @desc:

from django.db import models

# Create your models here.

class NetDiskUser(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.CharField(u'所属平台', max_length=256,default="default")
    username = models.CharField(u'用户名', max_length=256)
    systemUsername = models.CharField(u'系统用户名', max_length=256)
    cluster = models.CharField(u'集群',max_length=256)
    tokenWeb = models.CharField(u'令牌', max_length=128, blank=True, null=True)
    tokenGererateTimeWeb = models.IntegerField(u'web令牌生成时间戳', blank=True, null=True)
    tokenDesk = models.CharField(u'令牌', max_length=128, blank=True, null=True)
    tokenGererateTimeDesk = models.IntegerField(u'桌面令牌生成时间戳', blank=True, null=True)
    tokenValidityPeriod = models.IntegerField(u'令牌有效期', default=3600)

    class Meta:
        db_table = u'netDiskUser'
        verbose_name = u'网盘用户'
        verbose_name_plural = u"网盘用户"
        unique_together = ("cluster","username")

class NetDiskTrashbin(models.Model):
    id = models.AutoField(primary_key=True, max_length=12)
    cluster = models.CharField(u'所属集群', max_length=256)
    username = models.CharField(u'用户名', max_length=256)
    sourcePath = models.CharField(u'源路径', max_length=512)
    sourceFilename = models.CharField(u'源文件名称', max_length=256)
    trashFilename = models.CharField(u'回收站文件名', max_length=64)
    deleteTime = models.DateTimeField(u'删除时间', auto_now_add=True)

    class Meta:
        db_table = u'netDiskTrashbin'
        verbose_name = u'回收站'
        verbose_name_plural = u'回收站'