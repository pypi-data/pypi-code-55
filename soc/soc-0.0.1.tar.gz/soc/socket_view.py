from .request import Request

import abc


class SocketView(abc.ABC):
    """ Socket View abstract base class """

    @abc.abstractmethod
    def handler(self, request: Request):
        ...
