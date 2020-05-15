#
# Copyright (c) 2020-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" basic container types """

from ujotypes import UjoList, UjoMap

from .basic import UjsBase


class UjsList(UjsBase):
    name = "list"
    typeid = 0x30
    default_to_ujo = UjoList

    def __init__(self, typ):
        self.type = typ

    def __str__(self):
        return self.name + " of " + repr(self.type)

    def __repr__(self):
        return self.name + " of " + repr(self.type)


class UjsMap(UjsBase):
    name = "map"
    typeid = 0x31
    default_to_ujo = UjoMap

    def __init__(self, typ):
        self.type = typ

    def __str__(self):
        return self.name + " of " + repr(self.type)

    def __repr__(self):
        return self.name + " of " + repr(self.type)
