from cnvrg.modules.storage.base_storage import BaseStorage
# from cnvrg.modules.storage.storage import Storage
from cnvrg.modules.cnvrg_files import CnvrgFiles
from typing import Dict
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
import click
import os
import time
import threading
import multiprocessing
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Pool, Process, Manager
from multiprocessing.pool import ThreadPool
from functools import partial

config = TransferConfig(
    multipart_threshold=1024 * 25,
    max_concurrency=10,
    multipart_chunksize=1024 * 25,
    use_threads=True
)


class MinioStorage(BaseStorage):
    def __init__(self, element: CnvrgFiles, working_dir: str, storage_resp: Dict):
        super().__init__(element, working_dir, storage_resp.get("path_sts"))
        del storage_resp["path_sts"]
        props = self.decrypt_dict(storage_resp, keys=["sts_a", "sts_s", "sts_st", "bucket", "region", "endpoint"])
        self.s3props = {
            "endpoint_url": props.get("endpoint"),
            "aws_access_key_id": props.get("sts_a"),
            "aws_secret_access_key": props.get("sts_s"),
            "region_name": props.get("region")
        }
        self.bucket = props.get("bucket")
        self.region = props.get("region")
        self.client = self._get_client()

    def upload_single_file(self, file, target):
        try:
            client = self.client
            client.upload_file(file, self.bucket, target, Config=config)
        except ClientError as e:
            print(e)

    def _get_client(self):
        return boto3.client('s3', **self.s3props)
