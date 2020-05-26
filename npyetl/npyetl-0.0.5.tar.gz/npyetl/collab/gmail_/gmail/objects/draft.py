from typing import (
    Dict
)
from ._base_object import (
    _BaseObject
)
from .message import (
    BaseMessage,
    make_message
)


class Draft(_BaseObject):
    
    def __init__(self,
                 id: str,
                 message: Dict[str, object]):
        super().__init__(id)
        self._message = make_message(**message)
    
    @property
    def message(self) -> BaseMessage:
        return self._message
