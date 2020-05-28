# -*- coding:utf-8 -*-
import logging
import os
from etools.singleton_meta import SingletonMeta


class SuffixRemover(object, metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.suffixes = self.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', "suffix.txt"))

    def read(self, filename):
        result = set()
        if not os.path.exists(filename):
            self.logger.error("load suffixes from [%s] failed", filename)
            return result
        with open(filename, 'r') as sfile:
            for y in sfile:
                result.add(y.strip())
        return result

    def remove_suffix(self, text):
        while text and text[-1] in self.suffixes:
            text = text[:-1]
        return text


suffix_remover = SuffixRemover()


