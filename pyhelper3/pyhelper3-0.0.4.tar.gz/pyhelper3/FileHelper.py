#-*- coding:utf-8 -*-
import os
from hashlib import md5
import base64
class FileHelper:
    @staticmethod
    def get_file_md5(filename):
        ret = None
        i = 0
        if not os.path.isfile(filename):
            return None,None,None
        with open(filename,'rb') as f:
            while True:
                myhash = hashlib.md5()
                b = f.read(204800)
                if not b:
                    break
                myhash.update(b)
                yield myhash.hexdigest(),b,i
                i += 1
    @staticmethod
    def get_smallfile_md5(filename):
        ret = None
        if not os.path.isfile(filename):
            return None,None,None
        myhash = hashlib.md5()
        f = open(filename,'rb')
        b = f.read()
        myhash.update(b)
        f.close()
        return myhash.hexdigest(),b,os.path.splitext(filename)[-1][1:]
    @staticmethod
    def remove_file_dir(path,flag=True):
        if path:
            if flag:
                if os.path.isdir(path):
                    os.rmdir(path)
            else:
                if os.path.exists(path):  
                    os.remove(path)
    def get_stuffix_name(file_name,is_dot=True):
        '''
        '''
        if is_dot:
            return os.path.splitext(file_name)[-1]
        else:
            return os.path.splitext(file_name)[-1][1:]