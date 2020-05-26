from .._base_object import _BaseObject


class Attachment(_BaseObject):
    
    def __init__(self,
                 id: str,
                 size: int,
                 data: bytes):
        super().__init__(id)
        self._size = size
        self._data = data
    
    @property
    def size(self) -> int:
        return self._size
    
    @property
    def data(self) -> bytes:
        return self._data
