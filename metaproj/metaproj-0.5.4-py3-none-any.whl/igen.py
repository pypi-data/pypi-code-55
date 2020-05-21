# -*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import os

class IGen(metaclass=ABCMeta):

    @abstractmethod
    def generate(self, name):
        pass

    def mkdir(self, path):

        path = path.strip()
        if not os.path.exists(path):
            os.mkdir(path)
            return True
        return False
