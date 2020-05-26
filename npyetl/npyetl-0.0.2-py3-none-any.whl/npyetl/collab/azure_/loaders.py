from typing import(
    Iterable,
    Dict,
    Any,
    Union,
    Optional
)
#
import json
from datetime import datetime
import azure.common
import azure.core.exceptions
from azure.storage.blob import (
    BlobServiceClient
)
from azure.storage. filedatalake import (
    DataLakeServiceClient
)
from azure.storage.file import (
    FileService
)
from azure.cosmosdb.table import (
    TableService,
    Entity
)
#
from npyetl.internals.decorators import override
from npyetl.data import BaseDataBlock
from npyetl.load import BaseLoader


class LoaderAzureBlob(BaseLoader):
    """
    Loader for Azure Blob Storage files.
    """
    def __init__(self,
                 version: int = 2,
                 metadata: dict = None):
        super().__init__(metadata)
    
    @override(BaseLoader)
    def load(self,
             data_blocks: Iterable[BaseDataBlock],
             storage_account_name: str,
             storage_account_key: str,
             container_name: str,
             directory: str = '',
             overwrite: bool = True,
             upload_blob_kwargs: dict = None,
             extension: str = None,
             **kwargs) -> bool:
        """
        Creates, updates or overwrites a blob file in the given storage account.
        :param storage_account_name:
        :param storage_account_key:
        :param container_name:
        :param directory:
        :param overwrite:
        :param upload_blob_kwargs:
        """
        upload_blob_kwargs = upload_blob_kwargs or dict()
        blob_storage_url = 'https://%s.blob.core.windows.net/' % storage_account_name
        blob_service_client = BlobServiceClient(blob_storage_url, credential=storage_account_key)
        container_client = blob_service_client.get_container_client(container_name)
        for data_block in data_blocks:
            blob_path = directory + data_block.name + (extension if extension else '')
            blob_client = container_client.get_blob_client(blob_path)
            try:
                blob_client.upload_blob(data_block.__str__(), **upload_blob_kwargs)
            except azure.core.exceptions.ResourceExistsError:
                if overwrite:
                    blob_client.delete_blob()
                    blob_client.upload_blob(data_block.__str__(), **upload_blob_kwargs)
        return True


class LoaderAzureTable(BaseLoader):
    """
    Loader for Azure Table Storage.
    """
    def __init__(self,
                 version: int = 2,
                 metadata: dict = None):
        super().__init__(metadata)
    
    @override(BaseLoader)
    def load(self,
             data_blocks: Iterable[BaseDataBlock],
             storage_account_name: str,
             storage_account_key: str,
             table_name: str,
             partition_key: Optional[str] = None,
             row_key: Optional[str] = None,
             overwrite: bool = True,
             timeout: int = None,
             **kwargs) -> bool:
        """
        :param storage_account_name:
        :param storage_account_key:
        :param container_name:
        :param directory:
        :param overwrite:
        :param upload_blob_kwargs:
        """
        table_service = TableService(storage_account_name, storage_account_key)
        for data_block in data_blocks:
            entity = self._set_entity(data_block.records, partition_key, row_key)
            try:
                table_service.insert_entity(table_name, entity, timeout=timeout)
            except azure.core.exceptions.ResourceExistsError:
                table_service.update_entity(table_name, entity, timeout=timeout)
            except (TypeError, ValueError) as e:
                print(e)
                print('Entity badly formatted.')
            except azure.common.AzureHttpError:
                print('Azure HTTP error.')
        return True
    
    def _set_entity(self,
                    entity: dict,
                    partition_key: str,
                    row_key: str) -> dict:
        """
        :param entity: [description]
        :param partition_key: [description]
        :param row_key: [description]
        :return: [description]
        """
        if partition_key.startswith('$.'):
            partition_key_val = entity.get(partition_key[2:]) 
        else:
            partition_key_val = partition_key
        if row_key.startswith('$.'):
            row_key_val = entity.get(row_key[2:]) 
        else:
            row_key_val = row_key
        #
        entity['PartitionKey'] = partition_key_val
        entity['RowKey'] = row_key_val
        #
        for k, v in entity.items():
            if type(v) not in (str, float, int, bool, datetime):
                entity[k] = json.dumps(v)
        return entity


class LoaderAzureDataLake(BaseLoader):
    
    def __init__(self,
                 metadata: dict = None):
        super().__init__(metadata)
        
    @override(BaseLoader)
    def load(self,
             data_blocks: Iterable[BaseDataBlock],
             storage_account_name: str,
             storage_account_key: str,
             file_system_name: str,
             directory: str = '',
             overwirte: bool = True,
             append_data_kwargs: dict = None,
             **kwargs) -> bool:
        """
        :param storage_account_name:
        :param storage_account_key:
        :param data_blocks: the list of BaseDataBlock to load into the blob storage.
        :param file_system_name: the file system name where the blob is located.
        :param directory: the directory where the blob is located.
        :param overwrite: overwrite blob's previous content, defaults to True
        :return: boolean indicating a succesful load.
        """
        append_data_kwargs = append_data_kwargs or dict()
        storage_account_url = 'https://%s.dfs.core.windows.net/' % storage_account_name
        data_lake_service_client = DataLakeServiceClient(storage_account_url, credential=storage_account_key)
        file_system_client = data_lake_service_client.get_file_system_client(file_system_name)
        for data_block in data_blocks:
            file_path = directory + data_block.name
            file_client = file_system_client.get_file_client(file_path)
            data = data_block.__str__()
            file_client.append_data(data, offset=0, **append_data_kwargs)
            file_client.flush_data(offset=len(data))
        return True


class LoaderAzureFileShare(BaseLoader):
    """
    """
    def __init__(self,
                 metadata: dict = None):
        super().__init__(metadata)

    def load(self,
             data_blocks: Iterable[BaseDataBlock],
             storage_account_name: str,
             storage_account_key: str,
             share_name: str,
             directory: str,
             format: str = 'text',
             overwrite: bool = False,
             **kwargs) -> bool:
        """
        :param data_blocks: [description]
        :type data_blocks: List[BaseDataBlock]
        :param storage_account_name: [description]
        :type storage_account_name: str
        :param storage_account_key: [description]
        :type storage_account_key: str
        :param share_name: [description]
        :type share_name: str
        :param directory: [description]
        :type directory: str
        :param write_type: either 'text' or 'bytes', defaults to 'text'
        :type write_type: str, optional
        :return: [description]
        :rtype: bool
        """
        file_service = FileService(storage_account_name, storage_account_key)
        for data_block in data_blocks:
            if format == 'text':
                file_service.create_file_from_text(share_name, directory, data_block.name,
                                                   data_block.__str__())
            elif format == 'bytes':
                file_service.create_file_from_bytes(share_name, directory, data_block.name,
                                                    data_block.records)
            else:
                raise ValueError(f"format must be either 'text' or 'bytes', not '{format}'")
