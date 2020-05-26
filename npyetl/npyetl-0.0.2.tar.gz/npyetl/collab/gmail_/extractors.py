from typing import (
    Union,
    Iterable,
    Dict
)
import datetime
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import importlib
#
from npyetl.collab.gmail_ import gmail
from npyetl.extraction.extractor import BaseExtractor
from npyetl.load.loader import BaseLoader
from npyetl.data import DataBlock
from npyetl.internals import override


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def get_and_update_credentials(extractor_name: str,
                               loader_name: str,
                               params: dict) -> Credentials:
    """[summary]
    :param reader: [description]
    :type reader: BaseExtractor
    :param writer: [description]
    :type writer: BaseLoader
    :param params: [description]
    :type params: dict
    :return: [description]
    :rtype: Credentials
    """
    extractor = my_import(extractor_name)
    loader = my_import(loader_name)
    creds_bytes = next(extractor().extract(**params)).records
    creds = pickle.loads(creds_bytes)
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        loader().load([DataBlock(pickle.dumps(creds))], **params)
    return creds

def make_query(start_time: Union[datetime.datetime, int, float],
               end_time: Union[datetime.datetime, int, float],
               query: str = '',) -> str:
    """[summary]
    :param start_time: [description]
    :param end_time: [description]
    :param query: [description], defaults to ''
    :return: [description]
    """
    if isinstance(start_time, datetime.datetime):
        start_time = start_time.timestamp()
    if isinstance(end_time, datetime.datetime):
        end_time = end_time.timestamp()            
    return f"after:{int(start_time)} before:{int(end_time)} " + query


class ExtractorGmailMessage(BaseExtractor):

    @override(BaseExtractor)
    def extract(self,
                credentials: Dict[str, object],
                start_time: Union[datetime.datetime, int, float],
                end_time: Union[datetime.datetime, int, float],
                query: str = '',
                api_version: str = 'v1') -> Iterable[DataBlock]:
        """
        [summary]
        :param credentials: [description]
        :param start_time: [description]
        :param end_time: [description]
        :param query: [description], defaults to ''
        :param api_version: [description], defaults to 1
        :return: [description]
        """
        credentials = get_and_update_credentials(**credentials)
        api = gmail.Api(credentials, api_version)
        query = make_query(start_time, end_time, query)
        print(f"Extracting messages for query {query}")
        messages = api.get_messages(query=query, format='full')
        for message in messages:
            yield DataBlock(message, name=message.id) 
        
        
class ExtractorGmailThread(BaseExtractor):

    @override(BaseExtractor)
    def extract(self,
                credentials: Dict[str, Union[str, dict]],
                start_time: Union[datetime.datetime, float],
                end_time: Union[datetime.datetime, float],
                query: str = '',
                api_version: str = 'v1') -> Iterable[DataBlock]:
        """[summary]
        :param credentials: [description]
        :type credentials: dict
        :param start_time: [description]
        :type start_time: Union[datetime.datetime, float]
        :param end_time: [description]
        :type end_time: Union[datetime.datetime, float]
        :param query: [description], defaults to ''
        :type query: str, optional
        :param api_version: [description], defaults to 1
        :type api_version: int, optional
        :return: [description]
        :rtype: List[DataBlock]
        """
        credentials = get_and_update_credentials(**credentials)
        api = gmail.Api(credentials, api_version)
        query = make_query(start_time, end_time, query)
        threads = api.get_threads(query=query)
        for thread in threads:
            yield DataBlock(thread, name=thread.id) 
