# -*- coding: UTF-8 -*-

import boto3

"""
s3目录是否存在的判断和创建，key必须以/结尾
"""


class S3Command(object):
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key
        self.client = boto3.client('s3')

    def mkdir(self):
        self.client.put_object(Bucket=self.bucket, Key=self.key)
        print('init path:%s' % self.key)

    def is_exist(self):
        try:
            self.client.get_object(Bucket=self.bucket, Key=self.key)
            flag = True
        except Exception:
            flag = False
        return flag
