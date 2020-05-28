#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ContainerAlreadyExistsException(Exception):
    def __init__(self, container_name):
        self.container_name = container_name


class BlobAthenticationFailedException(Exception):
    def __init__(self, blob_name):
        self.blob_name = blob_name


class TableBatchExceedCapacityException(Exception):
    def __init__(self, storage_account_name, table_name):
        self.storage_account_name = storage_account_name
        self.table_name = table_name


class TableBatchDeleteForbiddenException(Exception):
    def __init__(self, storage_account_name, table_name):
        self.storage_account_name = storage_account_name
        self.table_name = table_name


class TableBatchDataframeTooLargeException(Exception):
    def __init__(self, dataframe_size):
        self.dataframe_size = dataframe_size


class DatabricksClusterIdNotFoundException(Exception):
    def __init__(self, cluster_id):
        self.cluster_id = cluster_id


class DatabricksClusterNameNotFoundException(Exception):
    def __init__(self, cluster_name):
        self.cluster_name = cluster_name
