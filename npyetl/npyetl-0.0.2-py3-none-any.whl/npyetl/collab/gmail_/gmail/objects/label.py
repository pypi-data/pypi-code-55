from __future__ import annotations
from typing import (
    NamedTuple,
    Dict
)
from ._base_object import (
    _BaseObject
)

class Label(_BaseObject):
    
    def __init__(self,
                 id: str,
                 name: str,
                 messageListVisibility: str,
                 labelListVisibility: str,
                 type: str,
                 messagesTotal: int,
                 messagesUnread: int,
                 threadsTotal: int,
                 threadsUnread: int,
                 color: Dict[str,str]):
        super().__init__(id)
        self._name = name
        self._message_list_visibility = messageListVisibility
        self._label_list_visibility = labelListVisibility
        self._type = type
        self._messages_total = messagesTotal
        self._messages_unread = messagesUnread
        self._threads_total = threadsTotal
        self._threads_unread = threadsUnread
        self._color = _Color(**color)

    @property
    def name(self) -> str:
        return self._name
        
    @property
    def message_list_visibility(self) -> str:
        return self._message_list_visibility
        
    @property
    def label_list_visibility(self) -> str:
        return self._label_list_visibility
        
    @property
    def type(self) -> str:
        return self._type
        
    @property
    def messages_total(self) -> int:
        return self._messages_total
        
    @property
    def messages_unread(self) -> int:
        return self._messages_unread
        
    @property
    def threads_total(self) -> int:
        return self._threads_total
        
    @property
    def threads_unread(self) -> int:
        return self._threads_unread
        
    @property
    def color(self) -> _Color:
        return self._color

        
class _Color(NamedTuple):
    """
    """
    textColor: str
    backgorundColor: str
    