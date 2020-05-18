#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: containers and blobs
"""
import urllib
from azure.core.exceptions import ResourceExistsError

from azure.storage.blob import (
    BlobServiceClient,
    BlobClient,
    ContainerClient,
    BlobType,
    BlobSasPermissions,
    generate_blob_sas,
)
from datetime import datetime, timedelta
import pandas as pd
import gzip

from taz.storage_account import StorageAccount
from taz.exception import BlobAthenticationFailedException


class Container:
    def __init__(self, storage_account, name):
        """Blob Container

        :param storage_account: storage account
        :type storage_account: taz.storage_account.StorageAccount
        :param name: container name
        :type name: str
        """
        self.storage_account = storage_account
        self.name = name

        try:
            self.client = self.storage_account.blob_service_client.create_container(
                self.name
            )
        except ResourceExistsError:
            self.client = self.storage_account.blob_service_client.get_container_client(
                self.name
            )

    def get_properties(self):
        """get container properties

        :return: container properties
        :rtype: azure.storage.blob.ContainerProperties
        """
        return self.client.get_container_properties()

    def delete(self):
        """delete Container

        :return: self obj
        :rtype: taz.blob.Container
        """
        self.storage_account.blob_service_client.delete_container(self.name)
        return self

    def list_blobs(self, prefix=None):
        """list blobs in container

        :param prefix: prefix of blobs to list, defaults to None
        :type prefix: str, optional
        :return: list of blobs properties
        :rtype: Iterable of azure.storage.blob.BlobProperties
            BloProperties fields:
            - name
            - container
            - metadata
            - size
            - last_modified
            (see Azure documentation for further details) 
        """
        return self.client.list_blobs(name_starts_with=prefix)


class Blob:
    def __init__(
        self,
        container,
        name,
        sas_url=None,
        sas_key=None,
        storage_account_name=None,
        storage_account=None,
    ):
        """define blob object
        
        :param container: container name
        :type container: str
        :param name: blob name
        :type name: str
        :param sas_url: sas url, defaults to None
        :type sas_url: str, optional
        :param sas_key: sas key (needs storage_account_name), defaults to None
        :type sas_key: str, optional
        :param storage_account_name: storage account name, defaults to None
        :type storage_account_name: str, optional
        :param storage_account: storage account object, defaults to None
        :type storage_account: taz.blob.StorageAccount, optional
        """
        self.storage_account = storage_account
        self.container = container
        self.name = name
        self.sas_url = sas_url
        self.storage_account = storage_account
        self.sas_key = sas_key
        self.storage_account_name = storage_account_name

        if self.storage_account:
            self.auth_mode = "storage_account_connection_string"
            self.client = self.storage_account.blob_service_client.get_blob_client(
                self.container, self.name
            )
        elif self.sas_url:
            self.auth_mode = "sas_url"
            self.client = BlobServiceClient(sas_url).get_blob_client(
                self.container, self.name
            )
        elif self.sas_key and self.storage_account_name:
            self.auth_mode = "sas_key"
            self.client = BlobServiceClient(
                "https://{}.blob.core.windows.net/{}".format(
                    self.storage_account_name, self.sas_key
                )
            ).get_blob_client(self.container, self.name)
        else:
            raise (BlobAthenticationFailedException(self.name))

    def get_sas_token(
        self, expiry=datetime.utcnow() + timedelta(hours=1), permission_string="racwd",
    ):
        """generate sas token for blob

        :param expiry: token expiration date, defaults to datetime.utcnow()+timedelta(hours=1)
        :type expiry: datetime.datetime, optional
        :param permission_string: blob access permissions, defaults "racwd" (read, add, create, write, delete)
        :type permission_string: str, optional
        :return: sas token
        :rtype: str
        """

        permission = BlobSasPermissions.from_string(permission_string)

        self.sas_token = generate_blob_sas(
            self.storage_account.name,
            self.container,
            self.name,
            account_key=self.storage_account.key,
            permission=permission,
            expiry=expiry,
        )
        return self.sas_token

    def get_url(
        self, expiry=datetime.utcnow() + timedelta(hours=1), permission_string="racwd",
    ):
        """get url with sas token to download blob

        :param expiry: token expiration date, defaults to datetime.utcnow()+timedelta(hours=1)
        :type expiry: datetime.datetime, optional
        :param permission: blob access permissions, defaults "racwd" (read, add, create, write, delete)
        :type permission: BlobSasPermissions, optional
        :return: blob url
        :rtype: str
        """
        return "{}?{}".format(
            self.client.url,
            self.get_sas_token(expiry=expiry, permission_string=permission_string),
        )

    def read(self):
        """read datas from blob
        
        datas neads to be decoded, example for utf8 text:
        myblob.read().decode("utf8")

        :return: binary data read
        :rtype: bytes
        """
        return self.client.download_blob().readall()

    def read_csv(self, **kargs):
        """read CSV file from Blob

        :param **kargs: all pandas.Dataframe.read_csv() params
        :type kargs: *
        :return: DataFrame filled with read datas
        :rtype:  pandas.DataFrame
        """
        return pd.read_csv(self.get_url(), **kargs)

    def gzip_write(self, data, overwrite=True):
        """write gzipped data to blob
        
        :param data: datas to write
        :type data: binary string
        :param overwrite: overwrite or not, defaults to True
        :type overwrite: bool, optional
        """
        return self.write(gzip.compress(data, compresslevel=9), overwrite=overwrite)

    def write(self, data, overwrite=True):
        """write data to blob

        :param data: data
        :type data: bytes
        :param overwrite: overwrite blob if existing, defaults to True
        :type overwrite: bool, optional
        :return: self obj
        :rtype: taz.blob.Blob
        """
        self.client.upload_blob(data, overwrite=overwrite)
        return self

    def upload(self, path, overwrite=True):
        """upload file to blob
        
        :param path: local path
        :type path: str
        :param overwrite: overwrite blob or not, defaults to True
        :type overwrite: bool, optional
        """
        with open(path, "rb") as data:
            self.write(data, overwrite=True)
        return self

    def download(self, path):
        """download blob to local file

        :param path: local path to write blob
        :type path: str
        :return: self obj
        :rtype: taz.blob.Blob
        """
        with open(path, "wb") as data:
            data.write(self.read())
        return self

    def delete(self):
        """delete blob

        :return: self obj
        :rtype: taz.blob.Blob
        """
        self.client.delete_blob()
        return self

    def add_metadata(self, metadata):
        """merge metadata to existing

        :param metadata: metadata to merge
        :type metadata: dict
        :return: self obj
        :rtype: taz.blob.Blob
        """
        new_metadata = self.get_metadata()
        new_metadata.update(metadata)
        self.set_metadata(new_metadata)
        return self

    def set_metadata(self, metadata: dict):
        """replace blob metadata

        :param metadata: metadata (if None, reset)
        :type metadata: dict
        """
        self.client.set_blob_metadata(metadata)
        return self

    def get_metadata(self):
        """get blob metadata

        :return: metadatas
        :rtype: dict
        """
        return self.get_properties().metadata

    def get_properties(self):
        """get all blob properties

        :return: blob proberties object
        :rtype: azure.storage.blob.BlobProperties
            BloProperties fields:
            - name
            - container
            - metadata
            - size
            - last_modified
            (see Azure documentation for further details) 
        """
        return self.client.get_blob_properties()

    def get_size(self):
        """get blob size

        :return: blob size (bytes)
        :rtype: int
        """
        return self.client.get_blob_properties().size
