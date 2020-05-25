from .host import HostName


class Protocol:

    __protocol: str

    def __init__(self, protocol: str):
        self.__protocol = protocol

    def __str__(self) -> str:
        return self.__protocol + '://'

    def __add__(self, other) -> str:
        return str(self) + other


class Url:

    __protocol: Protocol
    __host_name: HostName
    __url: str

    def __init__(self, protocol: Protocol, host_name: HostName):
        self.__protocol = protocol
        self.__host_name = host_name
        self.__url = None

    def __str__(self):
        if self.__url is None:
            self.__url = self.__protocol + str(self.__host_name)
        return self.__url

    def __add__(self, other) -> str:
        return str(self) + other
