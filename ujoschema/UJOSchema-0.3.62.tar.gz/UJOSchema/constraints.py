#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

# pylint: disable=super-init-not-called

""" constraints used in ujo schema """

from abc import ABC, abstractmethod


class UjsConstraint(ABC):
    """ base class for constraints """

    @abstractmethod
    def __repr__(self):
        pass


class UjsNotNull(UjsConstraint):
    typeid = 0x01

    def __init__(self):
        self.default = None

    def __repr__(self):
        s = "not null"
        if self.default is not None:
            s = s + " default " + repr(self.default)
        return s


class UjsOfLength(UjsConstraint):
    typeid = 0x02

    def __init__(self, length):
        self.length = length

    def __repr__(self):
        return "length( " + repr(self.length) + " )"

    def __iter__(self):
        return iter(self.length)


class UjsContains(UjsConstraint):
    typeid = 0x03

    def __init__(self, types):
        self.types = types

    def __repr__(self):
        return "of " + repr(self.types)


class UjsIn(UjsConstraint):
    typeid = 0x04

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return "in " + repr(self.values)

    def __iter__(self):
        return iter(self.values)


class UjsNotIn(UjsConstraint):
    typeid = 0x05

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return "not in " + repr(self.values)

    def __iter__(self):
        return iter(self.values)
