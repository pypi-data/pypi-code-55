from typing import (
    Union,
    Iterable,
    Optional
)
from datetime import (
    datetime,
    timedelta
)
import requests
import pandas as pd
from npyetl.extraction import BaseExtractor
from npyetl.data import (
    JSONDataBlock
)



class ExtractorOct8neChats(BaseExtractor):
    
    SERVER = 'backoffice-eu.oct8ne.com'
    ENDPOINT = f'https://{SERVER}/apidata/export/sessions/csv'
    DEMO = ''
    
    #@override(BaseExtractor)
    def extract(self,
                 domain_id: int,
                 api_token: str,
                 start_time: Union[datetime, int, float],
                 end_time: Union[datetime, int, float],
                 agent_filter: Optional[int] = None,
                 dept_filter: Optional[int] = None,
                 attention_filter: Optional[int] = None,
                 utc_offset: int = 1) -> Iterable[JSONDataBlock]:
        """
        :param domain_id: [description]
        :type domain_id: str
        :param api_token: [description]
        :type api_token: str
        :param start_time: [description]
        :type start_time: Union[datetime.datetime, int, float]
        :param end_time: [description]
        :type end_time: Union[datetime.datetime, int, float]
        """
        start_time = start_time if type(start_time)==datetime else datetime.fromtimestamp(start_time)
        end_time = end_time if type(end_time)==datetime else datetime.fromtimestamp(end_time)
        #
        request_url = (self.ENDPOINT + '?'
                                     + f'apiToken={api_token}' 
                                     + f'&domainId={domain_id}'
                                     + f'&startTime={start_time.strftime("%m/%d/%Y")}'
                                     + f'&endTime={end_time.strftime("%m/%d/%Y")}'
                                     + (f'&agentFilter={agent_filter}' if agent_filter else '')
                                     + (f'&deptFilter={dept_filter}' if dept_filter else '')
                                     + (f'&attentionFilter={attention_filter}' if attention_filter else '')
                                     + f'&utcOffset={utc_offset}')
        #
        #csv_content = requests.get(request_url).content
        print(request_url)
        for _, chat in pd.read_csv(request_url, sep=';', encoding="ISO-8859-1", error_bad_lines=False).iterrows():
            chat_datetime = datetime.strptime(f'{chat.Date} {chat.Time}', "%d/%m/%Y %H:%M")
            if start_time <= chat_datetime < end_time:
                yield JSONDataBlock(chat.to_dict(), name=chat.Id)
        
