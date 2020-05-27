#!/usr/bin/env python
# encoding: utf-8
# @author: LiChangsong&Tianyang
# @license: (C) Copyright 2013-2020/1/3, NSCC-TJ.AllRightsReserved.
# @contact: lics@nscc-tj.cn
# @software: 
# @file: errorList.py
# @time: 2020/1/3 11:15
# @desc:


errorCode = {######      通用错误码      ######
             'paramLack':1001,
             'timestampNotFit':1002,
             'wrongToken':1003,
             'tokenTimeOut':1004,
             ######      登录模块错误码      ######
             'WrongPasswd':1101,
             'UsernameNotExist':1102,
             'UsernameRepeat':1103,
             'UserNotActive':1104,
             ######      我的网盘模块错误码      ######
             'chunkCheckError':1201,
             'fileCheckError':1202,
             'serverPathNotExist':1203,
             'localPathNotExist':1204,
             'serverPathExists':1205,
             'localPathExist':1206,
             'filePermissionError':1207,
             'pathIsFile':1208,
             'invalidSortKey':1209,
             'mkdirFailed':1210,
             'deleteFileFailed':1211,
             'deleteDirFailed':1212,
             'sourcePathNotExist':1213,
             'destPathIsNotDir':1214,
             'copyFailed':1215,
             'cutFailed':1216,
             'destPathExists':1217,
             'destPathNotExists':1218,
             'fileObjectNotExists':1219,
             'tmpDestPathExists':1220,
             'canNotDeleteRootPath':1221,
             'sourcePathIsDir':1222,
             'chownFailed':1223,
             'duFailed':1224,
             'touchFailed':1225,
             'quotaExceeded':1226,
             'destInSource':1227,
             'fileCheckFailed':1228,
             'generateTmpLinkFailed':1229,
             ######      用户管理错误描述      ######
             'usernameExist':1301,
             }

errorDesc = {######      通用错误描述      ######
             'paramLack':'key %s is needed.',
             'timestampNotFit':'request time out, please check your clock.',
             'wrongToken':'token of user %s not right. please login again.',
             'tokenTimeOut':'token of user %s timeout, please login again.',
             ######      登录模块错误描述      ######
             'WrongPasswd':'wrong password for user %s',
             'UsernameNotExist':'user %s not exists.',
             'UsernameRepeat':'username %s repeat.',
             'UserNotActive': 'the user is not active',
             ######      我的网盘模块错误描述      ######
             'chunkCheckError':1201,
             'fileCheckError':1202,
             'serverPathNotExist':'server path not exist.',
             'localPathNotExist':1204,
             'serverPathExists':'server path exists.',
             'localPathExists':1206,
             'filePermissionError':1207,
             'pathIsFile':'server path is a file, not dir.',
             'invalidSortKey':'invalid sort key. only support fileName/size/mtime.',
             'mkdirFailed':'create new folder failed.',
             'deleteFileFailed':'delete file failed.',
             'deleteDirFailed':'delete dir failed.',
             'sourcePathNotExist':'source path not exists',
             'destPathIsNotDir':'dest path is not dir',
             'copyFailed':'copy file or dir failed.',
             'cutFailed':'cut file or dir failed.',
             'destPathExists':'dest path exists',
             'destPathNotExists':'dest path not exists',
             'fileObjectNotExists':'file object not exists',
             'tmpDestPathExists':'tmp dest path exists',
             'canNotDeleteRootPath': 'can not delete user\'s root path',
             'sourcePathIsDir': 'source path is dir.',
             'chownFailed': 'chown failed.',
             'duFailed': 'compute path size failed.',
             'touchFailed': 'touch a file failed.',
             'quotaExceeded': 'quota of user %s exceeded.',
             'destInSource': 'dest path is the sub path of source path.',
             'fileCheckFailed': 'file md5 check failed.',
             'generateTmpLinkFailed': 'generate the tmp download link failed.',
             ######      用户管理错误描述      ######
             'usernameExist': 'username exist',
             }

def getErrorCode(errorName):
    return errorCode[errorName]

def getErrorDesc(errorName, param1='', param2='', param3=''):
    if param3:
        return errorDesc[errorName] % (param1, param2, param3)
    elif param2:
        return errorDesc[errorName] % (param1, param2)
    elif param1:
        return errorDesc[errorName] % (param1)
    else:
        return errorDesc[errorName]

def generateError(errorName, param1='', param2='', param3=''):
    if param3:
        desc = errorDesc[errorName] % (param1, param2, param3)
    elif param2:
        desc = errorDesc[errorName] % (param1, param2)
    elif param1:
        desc = errorDesc[errorName] % (param1)
    else:
        desc = errorDesc[errorName]
    code = errorCode[errorName]
    return (code, desc)
