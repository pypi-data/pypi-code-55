#!/usr/bin/env python
# encoding: utf-8
# @author: Tianyang
# @license: (C) Copyright 2013-2020/1/3, NSCC-TJ.AllRightsReserved.
# @contact: tianyang@nscc-tj.cn
# @software: 
# @file: urls.py
# @time: 2020/1/3 11:06
# @desc:

"""THStorageDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from thStorage import views

router = DefaultRouter()
router.register(r'THNetDisk/login', views.UserLogin, 'UserLogin')
router.register(r'THNetDisk/logout', views.UserLogout, 'UserLogout')
#router.register(r'THNetdisk/updateQuota', views.UpdateQuota, base_name='UpdateQuota')
router.register(r'THNetDisk/list', views.ContentList, 'ContentList')
#router.register(r'THNetdisk/list2', views.ContentList2, base_name='ContentList2')
router.register(r'THNetDisk/capacity', views.Capacity, 'Capacity')
router.register(r'THNetDisk/newfolder', views.NewFolder, 'NewFolder')
router.register(r'THNetDisk/newFile', views.NewFile, 'NewFile')
router.register(r'THNetDisk/delete', views.Delete, 'Delete')
router.register(r'THNetDisk/copyTo', views.CopyTo, 'CopyTo')
router.register(r'THNetDisk/cutTo', views.CutTo, 'CutTo')
router.register(r'THNetDisk/rename', views.Rename, 'Rename')
router.register(r'THNetDisk/attribute', views.Attribute, 'Attribute')
router.register(r'THNetDisk/webUploadFile', views.webUploadFile, 'webUploadFile')
router.register(r'THNetDisk/uploadFile', views.UploadFile, 'UploadFile')
router.register(r'THNetDisk/downloadFile', views.DownloadFile, 'DownloadFile')
router.register(r'THNetDisk/webDownloadFile', views.WebDownloadFile, 'WebDownloadFile')
# router.register(r'addUser', views.AddUser, base_name='AddUser')

router.register(r'THNetDisk/trashDelete', views.TrashDelete, 'TrashDelete')
router.register(r'THNetDisk/trashList', views.TrashList, 'TrashList')
router.register(r'THNetDisk/trashRestore', views.TrashRestore, 'TrashRestore')
router.register(r'THNetDisk/trashCleanUp', views.TrashCleanUp, 'TrashCleanUp')
router.register(r'THNetDisk/trashAutoCleanUp', views.TrashAutoCleanUp, 'TrashAutoCleanUp')
router.register(r'THNetDisk/trashEmpty', views.TrashEmpty, 'TrashEmpty')
router.register(r'THNetDisk/UserInfo', views.UserInfo, 'UserInfo')

router.register(r'THNetDisk/deleteToTrash', views.DeleteToTrash, 'DeleteToTrash')
router.register(r'THNetDisk/listTrashObject', views.ListTrashObject, 'ListTrashObject')
router.register(r'THNetDisk/restoreTrashObject', views.RestoreTrashObject, 'RestoreTrashObject')
router.register(r'THNetDisk/cleanTrashCan', views.CleanTrashCan, 'CleanTrashCan')
router.register(r'THNetDisk/moveTrashObject', views.MoveTrashObject, 'MoveTrashObject')
router.register(r'THNetDisk/deleteTrashObject', views.DeleteTrashObject, 'DeleteTrashObject')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^THNetDisk/thstorage$',views.THStorage.as_view(),name="thstorage"),
]