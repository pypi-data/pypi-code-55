#
# Copyright (c) 2020-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" base classes for converters """

from abc import ABC, abstractmethod

# pylint: disable=abstract-method


class BaseConverter(ABC):
    @abstractmethod
    def convert(self):
        pass


class BaseSchemaConverter(BaseConverter, ABC):
    def __init__(self, schema):
        self.schema = schema


class BaseTypeConverter(BaseConverter, ABC):
    def __init__(self, schema, typ):
        self.schema = schema
        self.typ = typ


class BaseConstraintConverter(BaseConverter, ABC):
    def __init__(self, constraint):
        self.constraint = constraint


class BaseRangeConverter(BaseConverter, ABC):
    def __init__(self, range_):
        self.range = range_
