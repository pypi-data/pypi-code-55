#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: Azure Tables (Cosmos DB light)
"""

import datetime as datetime
import json
import pandas as pd

from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch as AzureTableBatch

from taz.storage_account import StorageAccount

from taz.exception import (
    TableBatchExceedCapacityException,
    TableBatchDeleteForbiddenException,
    TableBatchDataframeTooLargeException,
)


class Table:
    def __init__(self, table_name: str, storage_account: StorageAccount):
        """Table class

        :param table_name: name of table
        :type table_name: str
        :param storage_account: [description]
        :type storage_account: StorageAccount
        """
        self.name = table_name
        self.storage_account = storage_account

    def create(self):
        """create table
        do nothing if already exists

        :return: self obj
        :rtype: taz.table.Table
        """
        if not self.exists():
            self.storage_account.table_service_client.create_table(self.name)
        return self

    def exists(self):
        """test existance of table

        :return: Existance of table
        :rtype: bool
        """
        return self.storage_account.table_service_client.exists(self.name)

    def delete(self):
        """delete table

        :return: self obj
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.delete_table(self.name)
        return self

    def insert_entity(self, entity: dict):
        """insert entity

        :param entity: entity to insert (must content a PartitionKey and a RowKey)
        :type entity: dict
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.insert_entity(self.name, entity)
        return self

    def upsert_entity(self, entity: dict):
        """insert or replace entity

        :param entity: entity to upsert (must content a PartitionKey and a RowKey)
        :type entity: dict
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.insert_or_replace_entity(
            self.name, entity
        )
        return self

    def query_entities_to_dataframe(self, filter=None):
        """query entities to pandas Dataframe

        ODATA queries documentation:
        https://docs.microsoft.com/en-us/rest/api/storageservices/querying-tables-and-entities

        Example:
        "PartitionKey eq 'users' and RowKey gt 'Fauchard-' and RowKey lt 'Fauchard-z'"

        :param filter: odata request filter, defaults to None
        :type filter: str, optional
        :return: pandas dataframe
        :rtype: pd.Dataframe
        """
        return pd.DataFrame(self.query_entities(filter=filter))

    def query_entities(self, filter=None):
        """query entities

        ODATA queries documentation:
        https://docs.microsoft.com/en-us/rest/api/storageservices/querying-tables-and-entities

        Example:
        "PartitionKey eq 'users' and RowKey gt 'Fauchard-' and RowKey lt 'Fauchard-z'"

        :param filter: odata request filter, defaults to None
        :type filter: str, optional
        :return: entities
        :rtype: dict[]
        """
        return self.storage_account.table_service_client.query_entities(
            self.name, filter=filter,
        )

    def merge_entity(self, entity: dict):
        """insert or replace entity

        :param entity: entity to upsert (must content a PartitionKey and a RowKey)
        :type entity: dict
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.merge_entity(self.name, entity)
        return self

    def delete_entity(self, partition_key: str, row_key: str):
        """delete entity by partition and row keys

        :param partition_key: partition key
        :type partition_key: str
        :param row_key: row key
        :type row_key: str
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.delete_entity(
            self.name, partition_key=partition_key, row_key=row_key
        )
        return self

    def get_entity(self, partition_key: str, row_key: str):
        """get entity by partition and row keys

        :param partition_key: partition key
        :type partition_key: str
        :param row_key: row key
        :type row_key: str
        :return: selected entity
        :rtype: azure.storage.table.models.Entity (can be used as a dict)
        """
        return self.storage_account.table_service_client.get_entity(
            self.name, partition_key=partition_key, row_key=row_key
        )

    def __str__(self):
        return self.name


class TableBatch(Table):
    def __init__(
        self,
        table_name: str,
        storage_account: StorageAccount,
        max_tasks=100,
        auto_commit=False,
    ):
        """Batch Table Class

        Can write up to max_tasks entities (update or insert) 
        with a single request

        :param table_name: table to handle
        :type table_name: str
        :param storage_account: storage account
        :type storage_account: StorageAccount
        :param max_tasks: max tasks to handle, defaults to 100, max 100
        :type max_tasks: int, optional
        :param auto_commit: auto commit or not, defaults to False
        :type auto_commit: bool, optional
        """
        Table.__init__(self, table_name, storage_account)
        if max_tasks > 100:
            self.max_tasks = 100
        else:
            self.max_tasks = max_tasks
        self.auto_commit = auto_commit
        self.sessions = {}
        self._start_session()

    def _start_session(self):
        self.session_id = datetime.datetime.utcnow().isoformat()
        self.sessions[self.session_id] = {
            "state": "pending",
            "mode": "",
            "results": [],
            "submitted_tasks": [],
            "size": 0,
        }
        self.tasks_to_commit = 0
        self.batch = AzureTableBatch()

    def _add_task(self, type: str, partition_key: str, row_key: str):
        self.sessions[self.session_id]["submitted_tasks"].append(
            {"Type": type, "PartitionKey": partition_key, "RowKey": row_key}
        )
        return self

    def delete(self):
        raise TableBatchDeleteForbiddenException(self.storage_account.name, self.name)

    def commit_batch(self):
        """commit batch task

        :return: self
        :rtype: taz.table.BatchTable
        """
        self.sessions[self.session_id]["mode"] = "manual"
        self._commit_batch()
        return self

    def _commit_batch(self):
        if self.tasks_to_commit > 0:
            response = self.storage_account.table_service_client.commit_batch(
                self.name, self.batch
            )
            self.sessions[self.session_id]["size"] = self.tasks_to_commit
            self.sessions[self.session_id]["results"] = response
            self.sessions[self.session_id]["state"] = "committed"
            self._start_session()
        return self

    def _auto_commit(self):
        """private method to handle auto batch commit

        :raises TableBatchExceedCapacityException: if batch exceed capacity
        :return: self
        :rtype: TableBatch
        """
        if self.tasks_to_commit >= self.max_tasks:
            if self.auto_commit:
                self.sessions[self.session_id]["mode"] = "auto"
                self._commit_batch()
            else:
                raise TableBatchExceedCapacityException(
                    self.storage_account.name, self.name
                )
        self.tasks_to_commit += 1
        return self

    def insert_or_replace_entity(self, entity: dict):
        """replace entity is exists insert otherwise

        :param entity: entity to insert or replace
        (must include PartitionKey and RowKey)
        :type entity: dict
        :return: self
        :rtype: TableBatch
        """
        self._auto_commit()._add_task(
            "insert_or_replace", entity["PartitionKey"], entity["RowKey"]
        ).batch.insert_or_replace_entity(entity)

        return self

    def _check_dataframe_size(self, df: pd.DataFrame):
        if (
            df.shape[0] > (self.max_tasks - self.tasks_to_commit)
        ) and not self.auto_commit:
            raise TableBatchDataframeTooLargeException(df.shape[0])
        return self

    def insert_or_replace_entities_from_dataframe(self, df: pd.DataFrame):
        """batch insert or replace entities from dataframe

        :param df: pandas dataframe
        must include PartitionKey and RowKey column
        :type df: pd.DataFrame
        :return: self
        :rtype: TableBatch
        """
        self._check_dataframe_size(df)
        for entity in df.to_dict("records"):
            self.insert_or_replace_entity(entity)
        return self

    def merge_entities_from_dataframe(self, df: pd.DataFrame, if_match="*"):
        """batch merge entities from dataframe

        :param df: pandas dataframe
        must include PartitionKey and RowKey column
        :type df: pd.DataFrame
        :param if_match: concurency check 
        etag value or "*" for inconditionnal write, defaults to "*"
        :type if_match: str, optional
        :return: self
        :rtype: TableBatch
        """
        self._check_dataframe_size(df)
        for entity in df.to_dict("records"):
            self.merge_entity(entity, if_match=if_match)
        return self

    def insert_entities_from_dataframe(self, df: pd.DataFrame):
        """batch insert entities from dataframe
        no inserts if one entity exists

        :param df: pandas dataframe
        must include PartitionKey and RowKey column
        :type df: pd.DataFrame
        :return: self
        :rtype: TableBatch
        """
        self._check_dataframe_size(df)
        for entity in df.to_dict("records"):
            self.insert_entity(entity)
        return self

    def merge_entity(self, entity: dict, if_match="*"):
        """merge properties of existing and new entities

        :param entity: entity to merge
        (must include PartitionKey and RowKey)
        :type entity: dict
        :param if_match: concurency check 
        etag value or "*" for inconditionnal write, defaults to "*"
        :type if_match: str, optional
        :return: self
        :rtype: TableBatch
        """
        self._auto_commit()._add_task(
            "merge", entity["PartitionKey"], entity["RowKey"]
        ).batch.merge_entity(entity, if_match=if_match)

        return self

    def insert_entity(self, entity: dict):
        """insert entity
        raise an error if existing

        :param entity: entity to insert
        (must include PartitionKey and RowKey)
        :type entity: dict
        :return: self
        :rtype: TableBatch
        """
        self._auto_commit()._add_task(
            "insert", entity["PartitionKey"], entity["RowKey"]
        ).batch.insert_entity(entity)
        return self

    def delete_entity_from_dataframe(self, df: pd.DataFrame, if_match="*"):
        """batch delete entities from dataframe
        delete nothing if one entity doesn't exists

        :param df: pandas dataframe
        must include PartitionKey and RowKey column
        :type df: pd.DataFrame
        :param if_match: concurency check 
        etag value or "*" for inconditionnal write, defaults to "*"
        :type if_match: str, optional
        :return: self
        :rtype: TableBatch
        """
        self._check_dataframe_size(df)
        for entity in df.to_dict("records"):
            self.delete_entity(
                entity["PartitionKey"], entity["RowKey"], if_match=if_match
            )
        return self

    def delete_entity(self, partition_key: str, row_key: str, if_match="*"):
        """delete entity
        raise an error if not existing

        :param partition_key: value of PartitionKey property
        :type partition_key: str
        :param row_key: value of RowKey property
        :type row_key: str
        :param if_match: concurency check 
        etag value or "*" for inconditionnal write, defaults to "*"
        :type if_match: str, optional
        :return: self
        :rtype: TableBatch
        """
        self._auto_commit()._add_task(
            "delete", partition_key, row_key
        ).batch.delete_entity(partition_key, row_key, if_match=if_match)
        return self

    def update_entity(self, entity: dict, if_match="*"):
        """pdate entity
        raise an error in not existing

        :param entity: entity to update
        (must include PartitionKey and RowKey)
        :type entity: dict
        :param if_match: concurency check 
        etag value or "*" for inconditionnal write, defaults to "*"
        :type if_match: str, optional
        :return: self
        :rtype: TableBatch
        """
        self._auto_commit()._add_task(
            "update", entity["PartitionKey"], entity["RowKey"]
        ).batch.update_entity(entity, if_match=if_match)
        return self

    def get_stats_as_dataframe(self) -> pd.DataFrame:
        """get batch results as dataframe

        :return: Dataframe with all operations
        :rtype: pd.DataFrame
        """
        return pd.DataFrame(self.get_stats())

    def save_stats(self, table_name=None):
        """save stats in new table (name passed in table_name parameter
        or build from original table name with a suffixe "monitor")

        PartitionKey: "monitor"
        RowKey: SessionId + PartitionKey + RowKey

        :param table_name: [description], defaults to None
        :type table_name: [type], optional
        :return: [description]
        :rtype: [type]
        """
        if table_name is None:
            table_name = self.name + "monitor"
        df = self.get_stats_as_dataframe()
        df["RowKey"] = df["SessionId"] + "-" + df["PartitionKey"] + "-" + df["RowKey"]
        df["PartitionKey"] = "monitor"

        nested_batch = (
            TableBatch(
                table_name, auto_commit=True, storage_account=self.storage_account
            )
            .create()
            .insert_entities_from_dataframe(df)
            .commit_batch()
        )
        return self

    def get_stats(self):
        """results of all batch sessions

        :return: array of dicts with results
        :rtype: dict[]
        """
        entities = []
        for session_id in sorted(self.sessions.keys()):
            for i, task in enumerate(self.sessions[session_id]["submitted_tasks"]):
                entity = {
                    "SessionId": session_id,
                    "Type": task["Type"],
                    "PartitionKey": task["PartitionKey"],
                    "RowKey": task["RowKey"],
                    "CommitMode": self.sessions[session_id]["mode"],
                    "CommitState": self.sessions[session_id]["state"],
                }
                try:
                    entity["Result"] = self.sessions[session_id]["results"][i]
                except IndexError:
                    entity["Result"] = "unavailable"

                entities.append(entity)
        return entities
