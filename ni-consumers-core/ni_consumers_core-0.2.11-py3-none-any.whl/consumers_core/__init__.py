from abc import abstractmethod

from .common import extract_informations


class Action:

    @abstractmethod
    def execute(self, properties, body):
        pass
