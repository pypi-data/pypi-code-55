from abc import ABCMeta, abstractmethod


class BaseAction(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def execute(cls, *args, **kwargs):
        raise NotImplementedError
