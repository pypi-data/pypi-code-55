from typing import (
    List,
    Dict
)
from ._base_object import (
    _BaseObject
)
from .message import (
    make_message,
    BaseMessage
)


class Thread(_BaseObject):
    
    def __init__(self,
                 id: str,
                 historyId: str,
                 messages: List[Dict[str, object]]):
        super().__init__(id)
        self._history_id = historyId
        self._messages = [ make_message(**message) for message in messages ]
    
    @property
    def history_id(self) -> str:
        return self._history_id

    @property
    def messages(self) -> List[BaseMessage]:
        return self._messages
