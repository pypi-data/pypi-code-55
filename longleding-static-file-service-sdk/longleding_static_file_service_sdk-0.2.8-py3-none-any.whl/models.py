# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
from enum import unique, Enum

from .staticFileService_pb2 import (OSSBucketInfoMessage, UploadCredentialsMessage, StorageTypeEnum)


class StaticFileServiceException(Exception):
    pass


class OSSBucketInfo:

    def __init__(self, bucket_name: str, endpoint: str, bucket_url: str, storage_type: StorageTypeEnum):
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.bucket_url = bucket_url
        self.storage_type = storage_type

    @classmethod
    def from_pb(cls, oss_bucket_info: OSSBucketInfoMessage):
        return cls(oss_bucket_info.bucket_name, oss_bucket_info.endpoint, oss_bucket_info.bucket_url,
                   oss_bucket_info.storage_type)

    def _desc(self):
        return "<OSSBucketInfo(bucket_name:{} endpoint:{} bucket_url:{} storage_type:{})>".format(
            self.bucket_name,
            self.endpoint,
            self.bucket_url,
            self.storage_type
        )

    def __str__(self):
        return self._desc()

    def __repr__(self):
        return self._desc()


class UploadCredentials:

    def __init__(self, access_key_id: str, access_key_secret: str, expiration: datetime, security_token: str):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.expiration = expiration
        self.security_token = security_token

    @classmethod
    def from_pb(cls, upload_credentials: UploadCredentialsMessage):
        expiration = datetime.fromtimestamp(upload_credentials.expiration.seconds)
        expiration.replace(tzinfo=timezone(timedelta(hours=8)))
        return cls(upload_credentials.access_key_id,
                   upload_credentials.access_key_secret,
                   expiration,
                   upload_credentials.security_token)

    def _desc(self):
        return "<UploadCredentials(access_key_id:{} access_key_secret:{} expiration:{} security_token:{})>".format(
            self.access_key_id,
            self.access_key_secret,
            self.expiration,
            self.security_token
        )

    def __str__(self):
        return self._desc()

    def __repr__(self):
        return self._desc()


@unique
class BaseEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def value_list(cls):
        return [item.value for item in cls]

    @classmethod
    def parse_value(cls, value):
        for item in cls:
            if value == item.value:
                return item
        return None


class FileACLEnum(BaseEnum):
    """
    文件访问权限枚举
    """
    PRIVATE = 1  # 私有
    PUBLIC_READ = 2  # 公共读
    PUBLIC_READ_WRITE = 3  # 公共读写
    DEFAULT = 4  # 默认值，继承 Bucket 权限
