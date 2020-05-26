from typing import (
    Optional,
    Iterable
)
#
from azure.storage.blob import BlobServiceClient
from azure.cosmosdb.table import TableService
from azure.storage.queue import QueueService
from azure.storage.file import FileService
from azure.storage.file.models import (
    File,
    Share,
    Directory
)
#
from npyetl.internals.decorators import override
from npyetl.extraction import BaseExtractor
from npyetl.data import (
    BaseDataBlock,
    DataBlock,
    JSONDataBlock
)


class ExtractorAzureBlob(BaseExtractor):
    """
    Extractor for Azure Blob Storage blob files.
    """        
    def extract(self,
                storage_account_name: str,
                storage_account_key: str,
                container_name: str,
                directory: str = '',
                blob_name: str = None,
                **kwargs):
        """[summary]
        :param storage_account_name: [description]
        :type storage_account_name: str
        :param storage_account_key: [description]
        :type storage_account_key: str
        :param container_name: [description]
        :type container_name: str
        :param blob_name: [description]
        :type blob_name: str
        :param directory: [description], defaults to ''
        :type directory: str, optional
        """
        blob_storage_url = 'https://%s.blob.core.windows.net/' % storage_account_name
        blob_service_client = BlobServiceClient(blob_storage_url, credential=storage_account_key)
        container_client = blob_service_client.get_container_client(container_name)
        if blob_name:
            blob_client = blob_service_client.get_blob_client(container_name, directory+blob_name)
            download_stream = blob_client.download_blob()
            yield DataBlock(download_stream.readall(), name=blob_name)
        else:
            container_client = blob_service_client.get_container_client(container_name)
            for blob in container_client.list_blobs(name_starts_with=directory):
                blob_client = container_client.get_blob_client(blob.name)
                download_stream = blob_client.download_blob()
                yield DataBlock(download_stream.readall(), name=blob_name)
        return


class ExtractorAzureTable(BaseExtractor):
    """
    """
    def extract(self,
                storage_account_name: str,
                storage_account_key: str,
                table_name: str,
                filter: Optional[str] = None,
                select: Optional[str] = None,
                num_results: Optional[int] = None,
                **kwargs):
        """
        """
        table_service = TableService(storage_account_name, storage_account_key)
        for entity in table_service.query_entities(table_name, filter, select, num_results):
            yield JSONDataBlock(entity)
            

class ExtractorAzureQueue(BaseExtractor):
    """
    """
    def extract(self,
                storage_account_name: str,
                storage_account_key: str,
                queue_name: str,
                pop: bool = True,
                num_messages: Optional[int] = None,
                visibility_timeout: Optional[int] = None,
                timeout: Optional[int] = None,
                **kwargs):
        """
        """
        queue_service = QueueService()
        for message in queue_service.get_messages(queue_name, num_messages, visibility_timeout, timeout):
            yield DataBlock(message.content)
            if pop:
                queue_service.delete_message(queue_name, message.id, message.pop_receipt, timeout)


class ExtractorAzureFileShare(BaseExtractor):
    """
    Extractor for Azure File Share files.
    """        
    def extract(self,
                storage_account_name: str,
                storage_account_key: str,
                share_name: str,
                directory: str,
                file_name: Optional[str] = None,
                format: str = 'text',
                **kwargs) -> Iterable[BaseDataBlock]:
        """
        [summary]
        :param storage_account_name: [description]
        :type storage_account_name: str
        :param storage_account_key: [description]
        :type storage_account_key: str
        :param share_name: [description]
        :type share_name: str
        :param directory: [description]
        :type directory: str
        :param file_name: [description]
        :type file_name: str
        :param return_type: either 'text' or 'bytes', defaults to 'text'
        :type return_type: type, optional
        :return: [description]
        :rtype: BaseDataBlock
        """
        file_service = FileService(storage_account_name, storage_account_key)
        get_func = getattr(file_service, 'get_file_to_'+format)
        if file_name:
            print(share_name, directory, file_name)
            yield DataBlock(get_func(share_name, directory, file_name).content, name=file_name)
        #
        else:
            for file_or_dir in file_service.list_directories_and_files(share_name, directory):
                if isinstance(file_or_dir, File):
                    file_name = file_or_dir.name
                    yield DataBlock(get_func(share_name, directory, file_name).content, name=file_name)
        return
        