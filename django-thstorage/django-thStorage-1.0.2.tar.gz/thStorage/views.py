#!/usr/bin/env python
# encoding: utf-8
# @author: LiChangsong&Tianyang
# @license: (C) Copyright 2013-2020/1/3, NSCC-TJ.AllRightsReserved.
# @contact: lics@nscc-tj.cn
# @software: 
# @file: views.py
# @time: 2020/1/3 11:04
# @desc:
import json

from django.shortcuts import render
import datetime
import uuid
import time
import hashlib
import os
import pytz

from rest_framework import generics, permissions, renderers, viewsets
from django.utils.decorators import method_decorator
from django.shortcuts import render
from rest_framework.response import Response
from django.http import FileResponse
from django.conf import settings
from thStorage import models
from thStorage.errorList import generateError
from thStorage.thStorageClient import THSClient,LoginAuth,THStorageUser
from django.forms.models import model_to_dict
from django.views.generic import View

# Create your views here.

config = {
    'timestampInterval' :settings.TH_STORAGE_CONFIG['TOKEN_UPDATE_IMTERVAL'],
    'appid' :settings.TH_STORAGE_CONFIG['STORAGE_BACKEND_APPID'],
    'appkey' :settings.TH_STORAGE_CONFIG['STORAGE_BACKEND_APPKEY'],
    'server' :settings.TH_STORAGE_CONFIG['STORAGE_BACKEND_HOST']
}


def formatDate(date):
    dateString = date.split('+')[0].split('.')[0].replace('T', ' ').replace('Z', '')
    dateTime = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S')
    return dateTime


def CheckKeys(inputData, keyList=[]):
    '''
    检查inputData中是否包含keyList中的所有的key，如缺少某个key，报错缺少key。
    '''
    for key in keyList:
        if key not in inputData.keys():
            return {"status": 1, "lackKey": key}
    return {"status": 0}


def GenerateToken():
    '''
    生成一个32位的随机令牌
    '''
    random_str = str(uuid.uuid1())
    m = hashlib.md5()
    m.update(random_str)
    token = m.hexdigest().decode('utf-8')
    return token


def GenerateFailedResponse(errorInfo):
    '''
    根据错误码和错误描述，生成一个失败的消息。
    '''
    errorCode = errorInfo[0]
    errorDesc = errorInfo[1]
    print
    errorCode, errorDesc
    return Response({"success": "no",
                     "error_code": errorCode,
                     "error_desc": errorDesc})


def GenerateFailedResponse2(errorInfo):
    '''
    根据错误码和错误描述，生成一个失败的消息。
    '''
    errorCode = errorInfo['error_code']
    errorDesc = errorInfo['error_desc']
    return Response({"success": "no",
                     "error_code": errorCode,
                     "error_desc": errorDesc})

# class AddUser(viewsets.ViewSet):
#     def create(self, request):
#         inputData = request.data
#         keyList = ['cluster', 'username', 'password', 'totalCapacity']
#         checkKeys = CheckKeys(inputData, keyList)
#         if not checkKeys['status'] == 0:
#             lackKey = checkKeys['lackKey']
#             return GenerateFailedResponse(generateError('paramLack', lackKey))
#         cluster = inputData['cluster']
#         username = inputData['username']
#         password = inputData['password']
#         totalCapacity= inputData['totalCapacity']
#         if 'tokenValidityPeriod' in inputData.keys():
#             tokenValidityPeriod = inputData['tokenValidityPeriod']
#         else:
#             tokenValidityPeriod = 36000000
#         usedCapacity = 0
#         if models.NetDiskUser.objects.filter(cluster=cluster, username=username):
#             return GenerateFailedResponse(generateError('usernameExist', username))
#         models.NetDiskUser.objects.create(cluster=cluster,
#                                           username=username,
#                                           password=password,
#                                           tokenValidityPeriod=tokenValidityPeriod,
#                                           totalCapacity=totalCapacity,
#                                           usedCapacity=usedCapacity)
#         return Response({"success":"yes"})

# class UpdateQuota(viewsets.ViewSet):
#     def create(self, request):
#         '''
#         更新所有在7天内登录过的用户的空间使用信息
#         '''
#         users = models.NetDiskUser.objects.all()
#         for userInfo in users:
#             if userInfo.tokenGererateTime:
#                 timeNow = time.time()
#                 if (timeNow - float(userInfo.tokenGererateTime)) <= 604800:
#                     id = userInfo.id
#                     homePath = config['homePath']
#                     userHomePath = os.path.join(homePath, userInfo.username, 'files')
#                     try:
#                         #du_command = "du -sb %s | awk '{ print $1 }'" % userHomePath
#                         du_command = "diskus %s | awk -F\( '{ print $2 }' | awk '{ print $1 }'" % userHomePath
#                         result=os.popen(du_command).read()
#                         newUsedCapacity = int(result[0:len(result)-1])
#                     except:
#                         return GenerateFailedResponse(generateError('duFailed'))
#                     models.NetDiskUser.objects.filter(id=id).update(usedCapacity=newUsedCapacity)
#         return Response({"success":"yes"})

class UserLogin(viewsets.ViewSet):
    def create(self, request):
        '''
        验证用户登录请求是否合法，合法时返回token给用户
        '''
        inputData = request.data
        keyList = ['cluster', 'username', 'password']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        ##################################################################################

        ###                    各平台请在此插入自己平台的用户认证                         ###

        ##################################################################################
        # print "userlogin:", cluster, username
        # 认证通过，则生成token，并更新或插入数据库表。最后将token返回给前端
        token = GenerateToken()
        nowTime = int(time.time())
        if not models.NetDiskUser.objects.filter(cluster=cluster, username=username):
            models.NetDiskUser.objects.create(cluster=cluster,
                                              username=username,
                                              password='-',
                                              tokenValidityPeriod=36000000,
                                              tokenDesk=token,
                                              tokenGererateTimeDesk=nowTime, )
        else:
            models.NetDiskUser.objects.filter(cluster=cluster, username=username).update(tokenDesk=token,
                                                                                         tokenGererateTimeDesk=nowTime)
        return Response({"success": "yes", "token": token})


class UserLogout(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        处理用户登出请求
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', ]
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        console = inputData["console"]
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        token = GenerateToken()
        if console == 'desk':
            models.NetDiskUser.objects.filter(cluster=cluster, username=username).update(tokenDesk=token)
        elif console == 'web':
            models.NetDiskUser.objects.filter(cluster=cluster, username=username).update(tokenWeb=token)
        return Response({"success": "yes"})


class ContentList(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        获取用户某个目录下的所有文件和目录的列表信息。
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'path']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        path = inputData['path']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        # 获取可选参数
        if 'keyword' in inputData.keys() and inputData['keyword']:
            keyword = inputData['keyword']
        else:
            keyword = ''
        if 'sort' in inputData.keys() and inputData['sort']:
            sort = inputData['sort']
        else:
            sort = ''
        if 'sortDirection' in inputData.keys() and inputData['sortDirection'] == u'desc':
            desc = 1
        else:
            desc = 0
        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
        try:
            objs = client.listObjects(sort=sort, desc=desc, page=1, count=0, search=keyword)
            if 'objects' in objs.keys():
                for fileInfo in objs['objects']:
                    if fileInfo['name'] == '.trashbin':
                        objs['objects'].remove(fileInfo)

            if 'objects' in objs.keys() and objs['objects']:
                return Response({"success": "yes",
                                 "listLength": len(objs['objects']),
                                 "listContent": objs['objects']})
            else:
                return Response({"success": "yes",
                                 "listLength": 0,
                                 "listContent": []})
        except Exception as e:
            print
            "error:", e
            return Response({"success":"no", "error_desc":client.getError()})

class Capacity(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        查询用户当前的总空间和已使用空间
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', ]
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        # print "Capacity:", username, cluster
        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, '/')
        try:
            objs = client.getQuota()
            return Response({"success": "yes", "capacity": objs.get("groupQuota")})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})


class NewFile(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上创建一个新的空文件
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'serverPath', 'fileName']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        serverPath = inputData['serverPath'].replace('\\', '/')
        fileName = inputData['fileName']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        dir = 0
        path = os.path.join(serverPath, fileName)

        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
        try:
            client.createObject(dir=dir)
            return Response({"success": "yes"})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})


class NewFolder(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上创建一个新的目录
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'path']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        path = inputData['path'].replace('\\', '/')
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        dir = 1

        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
        try:
            client.createObject(dir=dir)
            return Response({"success": "yes"})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})


class Delete(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上，将删除一个目录或文件放到回收站
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'serverPathList']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        serverPathList = inputData['serverPathList']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        # 通过SDK，访问资源层接口
        try:
            for path in eval(serverPathList):
                # print path
                path = path.rstrip('/')
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
                client.deleteObject(recursive=1)
            return Response({"success": "yes"})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})


class CopyTo(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上复制一个或多个目录或文件。
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'oldPathList', 'newPath']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        oldPathList = inputData['oldPathList']
        newPath = inputData['newPath']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        for sourcePath in eval(oldPathList):
            if newPath.startswith(sourcePath):
                return Response({"success": "no", "error_desc": "目的地址不能是源地址的子目录"})

        failedList = []
        failedInfo = {}

        # 通过SDK，访问资源层接口
        for sourcePath in eval(oldPathList):
            try:
                path = os.path.join(newPath, os.path.basename(sourcePath))
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
                client.copyObject(sourcePath, recursive=1)
            except Exception as e:
                failedInfo['name'] = os.path.basename(sourcePath)
                failedInfo['reason'] = client.getError()
                failedList.append(failedInfo.copy())

        return Response({"success": "yes",
                         "failedList": failedList})


class CutTo(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上移动一个或多个目录或文件。
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'oldPathList', 'newPath']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        timestamp = inputData['timestamp']
        oldPathList = inputData['oldPathList']
        newPath = inputData['newPath']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        for sourcePath in eval(oldPathList):
            if newPath.startswith(sourcePath):
                return Response({"success": "no", "error_desc": "目的地址不能是源地址的子目录"})

        failedList = []
        failedInfo = {}

        # 通过SDK，访问资源层接口
        for sourcePath in eval(oldPathList):
            try:
                path = os.path.join(newPath, os.path.basename(sourcePath))
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
                client.moveObject(sourcePath, recursive=1)
            except Exception as e:
                failedInfo['name'] = os.path.basename(sourcePath)
                failedInfo['reason'] = client.getError()
                failedList.append(failedInfo.copy())

        return Response({"success": "yes",
                         "failedList": failedList})


class Rename(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上重命名一个或多个目录或文件。
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'path', 'oldName', 'newName']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        path = inputData['path']
        oldName = inputData['oldName']
        newName = inputData['newName']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        oldPath = os.path.join(path, oldName.strip('/'))
        newPath = os.path.join(path, newName.strip('/'))

        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, newPath)
        try:
            objs = client.moveObject(oldPath, recursive=1)
            return Response({"success": "yes"})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})


class Attribute(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        获取某个文件或目录的属性信息。
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'path']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        path = inputData['path']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
        try:
            objs = client.getObjectMeta()
            return Response({"success": "yes", "attribute": objs})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})


class UploadFile(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        上传一个文件。
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'fileName', 'serverPath',
                   'nowChunkNum', 'chunkNum', 'file']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        fileData = inputData['file']
        cluster = inputData['cluster']
        username = inputData['username']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        fileName = inputData['fileName']
        tmpFileName = fileName + '.thgyy.uploading'
        serverPath = inputData['serverPath'].replace('\\', '/')
        destPath = os.path.join(serverPath, fileName)
        tmpDestPath = os.path.join(serverPath, tmpFileName)

        nowChunkNum = int(inputData['nowChunkNum'])
        chunkNum = int(inputData['chunkNum'])

        # 如果serverPath不存在，则需要先创建
        # destFatherPath = os.path.join(config['homePath'], username, 'files', serverPath.strip('/'))
        # mkdir_command = "mkdir -p %s" % destFatherPath.replace(' ', '\ ').replace('(', '\(').replace(')', '\)')
        # try:
        # if not os.path.exists(destFatherPath):
        # result = os.system(mkdir_command)
        # if not result == 0:
        # return GenerateFailedResponse(generateError('mkdirFailed'))
        # except Exception:
        # return GenerateFailedResponse(generateError('mkdirFailed'))
        # chown_command="chown %s:%s %s" % ('apache', 'apache', destFatherPath.replace(' ', '\ ').replace('(', '\(').replace(')', '\)'))
        # try:
        # result = os.system(chown_command)
        # if not result == 0:
        # return GenerateFailedResponse(generateError('chownFailed'))
        # except:
        # return GenerateFailedResponse(generateError('chownFailed'))

        # destPath = os.path.join(config['homePath'], username, 'files', serverPath.strip('/'), fileName)
        # tmpDestPath = os.path.join(config['homePath'], username, 'files', serverPath.strip('/'), tmpFileName)
        # if os.path.exists(destPath) and nowChunkNum == 0:
        #     return GenerateFailedResponse(generateError('destPathExists'))
        # if os.path.exists(tmpDestPath) and nowChunkNum == 0:
        #     return GenerateFailedResponse(generateError('tmpDestPathExists'))

        # if nowChunkNum == 0:
        #     openMode = 'wb'
        # else:
        #     openMode = 'ab'
        # with open(tmpDestPath, openMode) as f:
        #     for chunk in fileData.chunks():
        #         f.write(chunk)
        # newUsedCapacity = int(usedCapacity) + len(fileData)
        # models.NetDiskUser.objects.filter(cluster=cluster, username=username).update(usedCapacity=str(newUsedCapacity))
        # if nowChunkNum + 1 == chunkNum:
        #     if 'fileMd5' in inputData.keys():
        #         fileMd5 = inputData['fileMd5']
        #         with open(tmpDestPath, 'rb') as ft:
        #             uploadFileMd5 = hashlib.md5()
        #             uploadFileMd5.update(ft.read())
        #             uploadFileMd5 = uploadFileMd5.hexdigest()
        #         if not fileMd5 == uploadFileMd5:
        #             return GenerateFailedResponse(generateError('fileCheckFailed'))
        #     shutil.move(tmpDestPath, destPath)
        #     chown_command="chown %s:%s %s" % ('apache', 'apache', destPath.replace(' ', '\ ').replace('(', '\(').replace(')', '\)'))
        #     try:
        #         result = os.system(chown_command)
        #         if not result == 0:
        #             return GenerateFailedResponse(generateError('chownFailed'))
        #     except:
        #         return GenerateFailedResponse(generateError('chownFailed'))
        # return Response({"success":"yes"})

        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, tmpDestPath)
        if nowChunkNum == 0:
            first = True
            for chunk in fileData.chunks():
                if first:
                    try:
                        print("upload location1")
                        objs = client.putObject(file=chunk)
                        print(objs)
                        print("upload location2")
                        first = False
                    except Exception as e:
                        print("1", e)
                        return Response({"error": client.getError()}, status=400)
                else:
                    try:
                        client.appendObject(file=chunk)
                    except Exception as e:
                        print("2", e)
                        return Response({"error": client.getError()}, status=400)
        else:
            for chunk in fileData.chunks():
                try:
                    client.appendObject(file=chunk)
                except Exception as e:
                    print("3", e)
                    return Response({"error": client.getError()}, status=400)

        if nowChunkNum + 1 == chunkNum:
            # 通过SDK，访问资源层接口
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, destPath)
            try:
                client.moveObject(tmpDestPath, recursive=1)
            except Exception as e:
                return Response({"error": client.getError()}, status=400)
                # if eval(str(e))['Code'] == 'ObjectNameExists':
                #    nowTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                #    newDestPath = newDestPath + "." + nowTime
                #    client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, newDestPath)
                #    try:
                #        objs = client.moveObject(destPath, recursive=1)
                #    except Exception as e:
                #        return Response({"success":"no",
                #                        "error_desc":eval(str(e))['Message']})

        return Response({"success": "yes"})


class webUploadFile(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'serverPath', 'file']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return Response({"error": 'paramLack'}, status=400)
        fileData = inputData['file']
        cluster = inputData['cluster']
        username = inputData['username']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        fileName = inputData['filename']
        # tmpFileName = fileName + '.thgyy.uploading'
        tmpFileName = fileName
        serverPath = inputData['serverPath'].replace('\\', '/')
        if serverPath == '/':
            destPath = os.path.join(serverPath, tmpFileName)
        else:
            destPath = os.path.join(serverPath.rstrip('/'), tmpFileName)
        chunkNumber = int(inputData['chunkNumber'])
        totalChunks = int(inputData['totalChunks'])
        totalSize = int(inputData['totalSize'])

        # 如果上传的是空文件，调用createObject接口
        if totalSize == 0:
            dir = 0
            path = os.path.join(serverPath, tmpFileName)
            # 通过SDK，访问资源层接口
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
            try:
                client.createObject(dir=dir)
                return Response({"success": "yes"})
            except Exception as e:
                return Response({"error": client.getError()}, status=400)

        # 通过SDK，访问资源层接口
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, destPath)
        if chunkNumber == 1:
            first = True
            for chunk in fileData.chunks():
                if first:
                    try:
                        client.putObject(file=chunk)
                        first = False
                    except Exception as e:
                        print("1", e)
                        return Response({"error": eval(str(e))['Code']}, status=400)

                else:
                    try:
                        client.appendObject(file=chunk)
                    except Exception as e:
                        print("2", e)
                        return Response({"error": client.getError()}, status=400)
        else:
            for chunk in fileData.chunks():
                try:
                    client.appendObject(file=chunk)
                except Exception as e:
                    print("3", e)
                    return Response({"error": client.getError()}, status=400)

        #
        # if chunkNumber == totalChunks:
        #    if serverPath == '/':
        #        newDestPath = os.path.join(serverPath, fileName)
        #    else:
        #        newDestPath = os.path.join(serverPath.rstrip('/'), fileName)
        #    # 通过SDK，访问资源层接口
        #    client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, newDestPath)
        #    try:
        #        objs = client.moveObject(destPath, recursive=1)
        #    except Exception as e:
        #        print eval(str(e))['Code']
        #        return Response({"error":eval(str(e))['Message']}, status=400)
        # if eval(str(e))['Code'] == 'ObjectNameExists':
        #    nowTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        #    newDestPath = newDestPath + "." + nowTime
        #    client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, newDestPath)
        #    try:
        #        objs = client.moveObject(destPath, recursive=1)
        #    except Exception as e:
        #        return Response({"success":"no",
        #                        "error_desc":eval(str(e))['Message']})

        return Response({"success": "yes"})


class DownloadFile(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        获取某个文件或目录的属性信息。
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'serverPath', 'startData', 'endData']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        serverPath = inputData['serverPath'].replace('\\', '/')
        fileName = os.path.basename(serverPath)
        startData = int(inputData['startData'])
        endData = int(inputData['endData'])

        # 通过SDK，访问资源层接口
        def file_iterator():
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, serverPath)
            offset = startData
            limit = endData - startData

            try:
                c = client.getObject(limit=limit, offset=offset)
                yield c
            except Exception as e:
                print
                e
                yield e

        # openMode = 'rb'
        # def file_iterator(sourcePath, chunk_size=4):
        #     with open(sourcePath, 'rb') as f:
        #         f.seek(startData)
        #         c = f.read(endData-startData)
        #         yield c
        response = FileResponse(file_iterator())
        response['content-type'] = 'application/octet-stream'
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName.encode('gbk'))
        # response['content-length'] = os.path.getsize(sourcePath)#传输给客户端的文件大小
        # if 'requestMd5' in  inputData.keys() and inputData['requestMd5']:
        #    with open(sourcePath, 'rb') as ft:
        #        filemd5 = hashlib.md5()
        #        filemd5.update(ft.read())
        #        filemd5 = filemd5.hexdigest()
        #        response['filemd5'] = filemd5
        return response


class WebDownloadFile(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def list(self, request):
        '''
        获取某个文件或目录的属性信息。
        '''
        inputData = request.GET
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'serverPath']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = request.GET.get('cluster')
        username = request.GET.get('username')
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        serverPath = request.GET.get('serverPath').replace('\\', '/')
        fileName = os.path.basename(serverPath)
        fileSize = ''

        # 通过SDK，访问资源层接口
        def file_iterator():
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, serverPath)
            fileSize = 0
            try:
                objs = client.getObjectMeta()
                fileSize = objs['size']
            except Exception as e:
                print
                e
            limit = 1048576
            chunkNum = 0
            while True:
                offset = chunkNum * limit
                if (fileSize - offset < limit):
                    limit = fileSize - offset
                try:
                    c = client.getObject(limit=limit, offset=offset)
                    yield c
                except Exception as e:
                    print
                    e
                if (fileSize - offset == limit):
                    break
                chunkNum += 1

        # print serverPath
        response = FileResponse(file_iterator())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName).encode('utf-8')
        response['Content-Length'] = fileSize  # 传输给客户端的文件大小
        response['filename'] = fileName.encode('utf-8')
        return response

        # 本次已将下载接口修改为GET，因此无需再使用如下方法。
        # 如果下载接口以POST的方法提供，则前台的下载可能会遇到问题。此时，可以用如下方法，先将下载文件放到static下一个临时目录中，然后将该路径生成一个下载链接，返回给客户端进行下载。
        # 生成链接文件路径和临时下载链接
        # todayDate = datetime.date.today().strftime('%Y%m%d')
        # encrypedTodayDate = hashlib.md5(todayDate).hexdigest()          # 为方便后期清除，所有连接文件均放在以当前日期命名的目录下，为不暴露，当天日期需经md5加密处理
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
        # todayDatePath = os.path.join(STATIC_ROOT, encrypedTodayDate)        #当天日期路径
        # randomStr = hashlib.md5(str(uuid.uuid1())).hexdigest()
        # linkFileFolder = os.path.join(todayDatePath, randomStr)              #链接文件所在目录
        # linkFilePath = os.path.join(linkFileFolder, fileName)                #链接文件全路径
        # tmpLink = os.path.join('https://wp.th-icloud.cn/static', encrypedTodayDate, randomStr, fileName)                         #临时下载链接

        # mkdirCommand = "mkdir -p %s" % linkFileFolder
        # try:
        #     if not os.path.exists(linkFileFolder):
        #         result = os.system(mkdirCommand)
        #         if not result == 0:
        #             return GenerateFailedResponse(generateError('mkdirFailed'))
        # except Exception:
        #     return GenerateFailedResponse(generateError('mkdirFailed'))
        # lnCommand = "ln -s %s %s" % (sourcePath, linkFilePath)
        # try:
        #     result = os.system(lnCommand)
        #     if not result == 0:
        #         return GenerateFailedResponse(generateError('generateTmpLinkFailed'))
        # except Exception:
        #     return GenerateFailedResponse(generateError('generateTmpLinkFailed'))

        # return Response({"success":"yes", "tmpLink":tmpLink})


class TrashDelete(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在服务器上删除一个目录或文件
        '''
        # inputData = json.loads(request.data.keys()[0])
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'serverPathList']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        timestamp = inputData['timestamp']
        serverPathList = inputData['serverPathList']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        # 创建回收站目录。创建失败时，如失败原因是“objectsexists”则不用理会，其他失败原因，报错退出
        trashbinPath = config['trashbinPath']
        client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, trashbinPath)
        try:
            objs = client.createObject(dir=1)
        except Exception as e:
            # print eval(str(e))
            if not eval(str(e))['Code'] == 'ObjectNameExists':
                return Response({"success": "no",
                                 "error_desc": eval(str(e))['Message']})

        # 通过SDK，访问资源层接口
        try:
            for path in eval(serverPathList):
                # 生成各种变量
                sourcePath = path.rstrip('/')
                sourceFilename = os.path.basename(sourcePath)
                trashFilename = hashlib.md5(str(uuid.uuid1())).hexdigest()
                trashPath = os.path.join(trashbinPath, trashFilename)
                # deleteTime = time.strftime('%Y-%m-%d %H:%M:%S')
                # 将文件move到回收站
                try:
                    client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username,
                                       trashPath)
                    objs = client.moveObject(sourcePath, recursive=1)
                except Exception as e:
                    return Response({"success": "no",
                                     "error_desc": eval(str(e))['Message']})
                # 将该条信息写入到数据库
                models.NetDiskTrashbin.objects.create(cluster=cluster,
                                                      username=username,
                                                      sourcePath=sourcePath,
                                                      sourceFilename=sourceFilename,
                                                      trashFilename=trashFilename)

            return Response({"success": "yes"})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": eval(str(e))['Message']})


class TrashList(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        返回回收站中的文件和目录列表
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        trashFilelist = []
        tList = models.NetDiskTrashbin.objects.filter(cluster=cluster, username=username).order_by('-deleteTime')
        for tInfo in tList:
            trashFileinfo = model_to_dict(tInfo)
            trashFileinfo['deleteTime'] = tInfo.deleteTime.strftime('%Y-%m-%d %H:%M:%S')
            expireTime = tInfo.deleteTime + datetime.timedelta(hours=24 * 7, minutes=0, seconds=0)
            remainDays = (expireTime - datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))).days + 1
            if (remainDays < 0):
                remainDays = 0
            trashFileinfo['remainDays'] = '剩余 ' + str(remainDays) + ' 天'
            trashFilelist.append(trashFileinfo.copy())

        return Response({"success": "yes", "trashFilelist": trashFilelist})


class TrashRestore(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        恢复一个文件或目录
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'trashInfolist']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        trashInfolist = inputData['trashInfolist']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        trashbinPath = config['trashbinPath']
        failedList = []
        failedInfo = {}
        destPath = ''

        # 通过SDK，访问资源层接口
        # client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
        for trashFileinfo in eval(trashInfolist):
            trashFilename = trashFileinfo['trashFilename']
            sourceFilename = trashFileinfo['sourceFilename']
            try:
                # 获取文件信息
                trashFileinfo = \
                models.NetDiskTrashbin.objects.filter(username=username, cluster=cluster, trashFilename=trashFilename)[
                    0]
                sourcePath = os.path.join(trashbinPath, trashFilename)
                destPath = trashFileinfo.sourcePath
                # 执行文件恢复操作
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, destPath)
                objs = client.moveObject(sourcePath, recursive=1)
                # 在数据库中将文件信息清除
                models.NetDiskTrashbin.objects.filter(username=username, cluster=cluster,
                                                      trashFilename=trashFilename).delete()
            except Exception as e:
                failedInfo['name'] = os.path.basename(sourceFilename)
                failedInfo['reason'] = eval(str(e))['Code']
                failedInfo['desc'] = eval(str(e))['Message']
                # print eval(str(e))['Message']
                failedList.append(failedInfo.copy())

        return Response({"success": "yes",
                         "failedList": failedList})


class TrashCleanUp(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        在回收站中，彻底删除一个文件或目录
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'trashInfolist']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        cluster = inputData['cluster']
        username = inputData['username']
        trashInfolist = inputData['trashInfolist']
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        trashbinPath = config['trashbinPath']
        failedList = []
        failedInfo = {}

        # 通过SDK，访问资源层接口
        for trashFileinfo in eval(trashInfolist):
            trashFilename = trashFileinfo['trashFilename']
            sourceFilename = trashFileinfo['sourceFilename']
            try:
                # 在数据库中将文件信息清除
                models.NetDiskTrashbin.objects.filter(username=username, cluster=cluster,
                                                      trashFilename=trashFilename).delete()
                # 执行文件删除操作
                path = os.path.join(trashbinPath, trashFilename)
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
                objs = client.deleteObject(recursive=1)
            except Exception as e:
                # print e
                failedInfo['name'] = os.path.basename(sourceFilename)
                failedInfo['reason'] = eval(str(e))['Code']
                failedList.append(failedInfo.copy())

        return Response({"success": "yes",
                         "failedList": failedList})


class TrashEmpty(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        清空回收站
        '''
        inputData = request.data
        cluster = inputData.get("cluster")
        username = inputData.get("username")
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################

        trashbinPath = config['trashbinPath']

        # 通过SDK，访问资源层接口
        try:
            # 清空数据库表
            models.NetDiskTrashbin.objects.all().delete()
        except Exception as e:
            return Response(
                {"success": "no", "error_code": "failed to empty database", "error_desc": "failed to empty database"})
        try:
            # 清空回收站
            path = trashbinPath
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
            objs = client.deleteObject(recursive=1)
        except Exception as e:
            print
            "empty trashbin failed, reason:%s" % e

        return Response({"success": "yes"})


class TrashAutoCleanUp(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        '''
        自动清除回收站中的过期文件
        '''
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        # 获取可选参数
        trashbinPath = config['trashbinPath']
        failedList = []
        failedInfo = {}
        nowTime = datetime.datetime.now()
        expireTime = nowTime - datetime.timedelta(hours=24 * 7, minutes=0, seconds=0)

        # 从数据库中查询过期文件列表
        tList = models.NetDiskTrashbin.objects.filter(deleteTime__lt=expireTime)
        for trashFileinfo in tList:
            # 从查询结果中，获取文件信息
            trashFilename = trashFileinfo.trashFilename
            sourceFilename = trashFileinfo.sourceFilename
            cluster = trashFileinfo.cluster
            username = trashFileinfo.username
            path = os.path.join(trashbinPath, trashFilename)
            try:
                # 删除数据库中的信息项
                models.NetDiskTrashbin.objects.filter(username=username, cluster=cluster,
                                                      trashFilename=trashFilename).delete()
                # 删除文件
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
                objs = client.deleteObject(recursive=1)
            except Exception as e:
                failedInfo['name'] = sourceFilename
                failedInfo['reason'] = eval(str(e))['Code']
                failedList.append(failedInfo.copy())

        return Response({"success": "yes",
                         "failedList": failedList})

class UserInfo(viewsets.ViewSet):
    def create(self, request):
        '''
        用户登录信息获取
        '''
        token = request.session.get("THNetDiskToken")
        username = request.session.get("username")
        cluster = request.session.get("cluster")
        systemUsername = request.session.get("systemUsername")
        tokenExpiredTime = request.session.get("THNetDiskTokenCreateTime",int(time.time())) # 当前时间
        if tokenExpiredTime - int(time.time()) > config["timestampInterval"]:
            thStorageUser = THStorageUser(username, cluster, systemUsername)
            token,user,c,sysUser = thStorageUser.Login()
            request.session["THNetDiskToken"] = token
        #for develop test
        #token = "5bc23a96ce4be1f5f14ebdb1f2e6c09f"
        #print(request.META['HTTP_HOST'])
        #systemUsername="test"
        #cluster="cluster"
        realHost = request.META['HTTP_HOST']
        return Response({"success": "yes",
                         "username": systemUsername,"cluster":cluster,"token":token,"remoteHost":realHost})

class DeleteToTrash(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp','serverPathList']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        cluster = inputData['cluster']
        username = inputData['username']
        serverPathList = inputData['serverPathList']
        # 通过SDK，访问资源层接口
        try:
            for path in eval(serverPathList):
                print(path)
                path = path.rstrip('/')
                client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, path)
                client.deleteObjectToTrash()
            return Response({"success": "yes"})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})

class ListTrashObject(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        cluster = inputData['cluster']
        username = inputData['username']
        try:
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, "")
            trashObjects = client.listTrashObject()
            return Response({"success": "yes","trashObjects":trashObjects["objects"]})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})

class RestoreTrashObject(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp','trashObjects']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        cluster = inputData['cluster']
        username = inputData['username']
        reqTrashObjects = inputData['trashObjects']
        # print(type(reqTrashObjects))
        # print(json.loads(reqTrashObjects))
        reqTrashObjects = json.loads(reqTrashObjects)
        try:
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, "")
            for trashObj in reqTrashObjects:
                print(trashObj['trashFileName'])
                client.restoreTrashObject(trashObj['trashFileName'])
            trashObjects = client.listTrashObject()
            return Response({"success": "yes", "trashObjects": trashObjects["objects"]})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})

class MoveTrashObject(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'trashObjects','path']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        cluster = inputData['cluster']
        username = inputData['username']
        reqTrashObjects = inputData['trashObjects']
        print(type(reqTrashObjects))
        print(json.loads(reqTrashObjects))
        reqTrashObjects = json.loads(reqTrashObjects)
        path = inputData['path']
        try:
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, "")
            for trashObj in reqTrashObjects:
                print(trashObj)
                client.setPath(path + '/' + trashObj['originalFileName'])
                client.moveTrashObject(trashObj['trashFileName'])
            trashObjects = client.listTrashObject()
            return Response({"success": "yes", "trashObjects": trashObjects["objects"]})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})

class DeleteTrashObject(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp', 'trashObjects']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        cluster = inputData['cluster']
        username = inputData['username']
        reqTrashObjects = inputData['trashObjects']
        # print(type(reqTrashObjects))
        # print(json.loads(reqTrashObjects))
        reqTrashObjects = json.loads(reqTrashObjects)
        try:
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, "")
            for trashObj in reqTrashObjects:
                # print(trashObj)
                client.deleteTrashObject(trashObj['trashFileName'])
            trashObjects = client.listTrashObject()
            return Response({"success": "yes", "trashObjects": trashObjects["objects"]})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})

class CleanTrashCan(viewsets.ViewSet):
    @method_decorator(LoginAuth)
    def create(self, request):
        inputData = request.data
        keyList = ['console', 'cluster', 'username', 'encrypedToken', 'timestamp']
        checkKeys = CheckKeys(inputData, keyList)
        if not checkKeys['status'] == 0:
            lackKey = checkKeys['lackKey']
            return GenerateFailedResponse(generateError('paramLack', lackKey))
        ################   ↑↑↑↑↑↑   以上常规检查工作结束   ↑↑↑↑↑↑   ###################
        cluster = inputData['cluster']
        username = inputData['username']
        try:
            client = THSClient(config['appid'], config['appkey'], config['server'], cluster, username, "")
            client.cleanTrashCan()
            trashObjects = client.listTrashObject()
            return Response({"success": "yes", "trashObjects": trashObjects["objects"]})
        except Exception as e:
            return Response({"success": "no",
                             "error_desc": client.getError()})

class THStorage(View):
    def get(self,request):
        return render(request, "thStorage.html")