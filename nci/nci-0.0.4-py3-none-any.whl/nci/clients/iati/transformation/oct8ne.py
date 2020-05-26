import pandas as pd
from typing import (
    Dict,
    Iterable,
    Optional
)
from npyetl.transformation import BaseTransformer
from npyetl.data import (
    DataBlock,
    JSONDataBlock
)


class TransformerOct8neChats(BaseTransformer):
    
    def transform(self,
                  data_blocks: Iterable[JSONDataBlock],
                  rename: Optional[Dict[str,str]] = None) -> Iterable[JSONDataBlock]:
        """
        :param data_blocks: [description]
        :type data_blocks: Iterable[JSONDataBlock]
        :return: [description]
        :rtype: Iterable[JSONDataBlock]
        """
        for data_block in data_blocks:
            yield JSONDataBlock(self.parse_chat(data_block.records, rename),
                                name=data_block.name)
        return
        
    def parse_chat(self,
                   chat: Dict[str,object],
                   rename: Optional[Dict[str,str]] = None) -> Dict[str,object]:
        """
        :param chat: [description]
        :type chat: Dict[str,object]
        :return: [description]
        :rtype: JSONDataBlock
        """
        # Correcting typo of Oct8ne API v1
        chat['Entry Point'] = chat.pop('Entery Point')
        if rename:
            for k, new_k in rename.items():
                chat[new_k] = chat.pop(k)
        for k, v in chat.items():
            if pd.isna(v) or v == '-':
                chat[k] = None
        return chat
