# -*- coding: utf-8 -*-

import codecs
import six
from iqsopenapi.core.IStrategyLoader import *

from iqsopenapi.util.logutil import *

def compile_strategy(source_code, strategy, scope):
    try:
        code = compile(source_code, strategy, 'exec')
        six.exec_(code, scope)
        return scope
    except Exception as e:
        logger.exception(e)

class FileStrategyLoader(IStrategyLoader):
    def __init__(self, strategy_file_path):
        self._strategy_file_path = strategy_file_path

    def load(self, scope):
        with codecs.open(self._strategy_file_path, encoding="utf-8") as f:
            source_code = f.read()

        return compile_strategy(source_code, self._strategy_file_path, scope)


class SourceCodeStrategyLoader(IStrategyLoader):
    def __init__(self, code):
        self._code = code

    def load(self, scope):
        return compile_strategy(self._code, "strategy.py", scope)


class UserFuncStrategyLoader(IStrategyLoader):
    def __init__(self, user_funcs):
        self._user_funcs = user_funcs

    def load(self, scope):
        for user_func in six.itervalues(self._user_funcs):
            user_func.__globals__.update(scope)
        scope.update(self._user_funcs)
        return self._user_funcs

if __name__ == '__main__':

    loader = FileStrategyLoader(r'D:\gitwork\inquantstudio\IQSOpenApi\IQS.OpenApi.Python\iqsopenapi\example\teststrategy.py')

    from iqsopenapi import *
    from copy import copy

    scope = copy(iqsopenapi.__dict__)

    loader.load(scope)

    pass