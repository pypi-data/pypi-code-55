from typing import List


class AccessInfo(object):
    __active: bool = True
    __exp: int = None
    __authorities: List[str] = []
    __client_id: str = None
    __scope: str

    def __init__(self, active: bool, exp: int, authorities: List[str], client_id: str, scope: str):
        self.__active = active
        self.__exp = exp
        self.__client_id = client_id
        self.__authorities = authorities
        self.__scope = scope

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def exp(self) -> int:
        return self.__exp

    @property
    def authorities(self) -> List[str]:
        return self.__authorities

    @property
    def client_id(self) -> str:
        return self.__client_id

    @property
    def scope(self) -> str:
        return self.__scope
