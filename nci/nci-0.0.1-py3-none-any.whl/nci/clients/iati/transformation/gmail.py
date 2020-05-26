import unicodedata
from typing import (
    Dict,
    List,
    Iterable,
    Optional
)
from npyetl.transformation import BaseTransformer
from npyetl.data import (
    DataBlock,
    JSONDataBlock
)


class TransformerIatiGmailMessage(BaseTransformer):
    
    def transform(self,
                  data_blocks: Iterable[DataBlock],
                  country: str,
                  categories: Dict[str,List[str]] = None):
        """[summary]
        :param data_blocks: [description]
        :type data_blocks: Iterable[DataBlock]
        :param categories: [description]
        :type categories: Dict[str,List[str]]
        :yield: [description]
        :rtype: [type]
        """
        for data_block in data_blocks:
            yield JSONDataBlock(parse_message(data_block.records, country, categories),
                                name=data_block.name)
        return


def parse_message(message: 'FullMessage',
                  country: str,
                  categories: Dict[str,List[str]] = None) -> Dict[str, object]:
    """[summary]
    :param message: [description]
    :type message: FullMessage
    :return: [description]
    :rtype: str
    """
    return {
        'id': message.id,
        'thread_id': message.thread_id,
        'label_ids': message.label_ids,
        'history_id': message.history_id,
        'snippet': message.snippet,
        'datetime': message.datetime.__str__(),
        'body': message.to_string(),
        'from': message.from_,
        'to': message.to,
        'subject': message.subject,
        'agent': get_agent(message, country),
        'category': get_category(message, categories),
        'sent': message.sent,
        'headers': message.payload.headers
    }

def get_agent(message: 'FullMessage', country: str) -> Optional[str]:
    """"[summary]"
    :param message: [description]
    :type message: [type]
    """
    if not message.sent:
        return None
    s = message.to_string()
    start, ends = '[image: logotipo IATI]', ['Departamento', 'Dpto.', 'Apoio ao Client']
    #
    i_start = s.find(start)
    for end in ends:
        i_end = s[i_start:].find(end)
        if i_end != -1:
            i_end += i_start
            break
    #
    if i_start != -1 and i_end != -1:
        return s[i_start+len(start):i_end].strip() or None
    return None

def get_category(message: 'FullMessage',
                 categories: Dict[str,List[str]]) -> Optional[str]:
    """[summary]
    :param message: [description]
    :type message: FullMessage
    :return: [description]
    :rtype: Optional[str]
    """
    if not categories:
        return None
    subject = strip_accents(message.subject).lower()
    for category, substrings in categories.items():
        if any([ strip_accents(substring).lower() in subject for substring in substrings ]):
            return category
    return None

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')