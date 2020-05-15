#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" objects """

from .typedef import TypedefBase, Typedef


class Object(TypedefBase):
    typeid = 0xE1

    def __init__(self, name, typ, items):
        super().__init__(name)
        self.type = typ
        self.items = items
        self.extends = None

    def __str__(self):
        s = self.name + " object of " + repr(self.type) + "{" + str(self.items) + "}"
        if self.extends is not None:
            s = s + " extends " + repr(self.extends)
        return s

    def __repr__(self):
        s = self.name + " object of " + repr(self.type) + "{" + str(self.items) + "}"
        if self.extends is not None:
            s = s + " extends " + repr(self.extends)
        return s

    def __iter__(self):
        return iter(self.items)


class ObjectItem(Typedef):
    def __init__(self, key, typ):
        super().__init__(str(key), typ)
        self.key = key
        self.optional = False

    def __repr__(self):
        if self.optional:
            s = "?"
        else:
            s = ""
        s = s + repr(self.key) + "->" + repr(self.type) + "::" + repr(self.constraint)
        if self.doc:
            s = s + "::doc '" + self.doc + "'"
        return s
