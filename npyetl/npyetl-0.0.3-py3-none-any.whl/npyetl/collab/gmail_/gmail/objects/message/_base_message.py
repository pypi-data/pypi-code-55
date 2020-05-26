from typing import (
    List,
    Dict,
    Optional
)
from abc import (
    ABC,
    abstractproperty
)
import json
import email
from datetime import datetime
from .._base_object import _BaseObject


class BaseMessage(_BaseObject):
    
    def __init__(self,
                 id: str,
                 threadId: str,
                 labelIds: List[str],
                 snippet: str,
                 historyId: str,
                 internalDate: str,
                 sizeEstimate: int):
        super().__init__(id)
        self._thread_id = threadId
        self._label_ids = labelIds
        self._snippet = snippet
        self._history_id = historyId
        self._internal_date = int(internalDate)
        self._size_estimate = sizeEstimate

    @property
    def email_message(self) -> email.message.Message:
        return email.message.Message()

    @property
    def thread_id(self) -> str:
        return self._thread_id

    @property
    def label_ids(self) -> List[str]:
        return self._label_ids

    @property
    def sent(self) -> bool:
        return 'SENT' in self._label_ids
    
    @property
    def snippet(self) -> str:
        return self._snippet

    @property
    def history_id(self) -> str:
        return self._history_id

    @property
    def internal_date(self) -> int:
        return self._internal_date
    
    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.internal_date/1000)

    @property
    def size_estimate(self) -> int:
        return self._size_estimate
