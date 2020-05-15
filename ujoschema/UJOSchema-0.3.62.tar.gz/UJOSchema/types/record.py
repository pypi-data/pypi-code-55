#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" records """

from .typedef import TypedefBase, Typedef


class Record(TypedefBase):
    typeid = 0xE0

    def __init__(self, name):
        super().__init__(name)
        self.items = []
        self.doc = ""
        self.extends = None

    def __repr__(self):
        s = self.name
        if self.extends is not None:
            s = s + " extends " + repr(self.extends)
        s = s + repr(self.items)
        if self.doc:
            s = s + "::doc '" + self.doc + "'"
        return s

    def __iter__(self):
        return iter(self.items)


class RecordItem(Typedef):
    pass
