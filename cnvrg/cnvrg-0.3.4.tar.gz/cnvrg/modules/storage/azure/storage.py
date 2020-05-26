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
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
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


class AzureStorage(BaseStorage):
    def __init__(self, element: CnvrgFiles, working_dir: str, storage_resp: Dict):
        super().__init__(element, working_dir, storage_resp.get("sts"))
        del storage_resp["sts"]
        props = self.decrypt_dict(storage_resp, keys=["container", "storage_access_key", "storage_account_name"])
        account_name = props["storage_account_name"]
        accout_key = props["storage_access_key"]
        self.access_key = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(account_name, accout_key)
        self.container_name = "jenkins"
        self.account_name = "cnvrg-dev"
        self.client = self._get_client()

    def upload_single_file(self, file, target):
        try:
            service = self.client
            client = service.get_blob_client(self.container_name, blob=target)
            with open(file, "rb") as data:
                client.upload_blob(data, overwrite=True)
        except ClientError as e:
            print(e)

    def _get_client(self):
        return BlobServiceClient.from_connection_string(self.access_key)
