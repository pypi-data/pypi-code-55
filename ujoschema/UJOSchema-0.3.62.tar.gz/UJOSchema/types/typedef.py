#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" type definitions """

from UJOSchema.types.container import UjsList

from .basic import UjsBase


class TypedefBase:
    def __init__(self, name):
        self.name = name
        self.doc = None


class Module(TypedefBase):
    def __repr__(self):
        s = "module " + self.name
        if self.doc:
            s = s + "::doc '" + self.doc + "'"
        return s


class Typedef(TypedefBase):
    def __init__(self, name, typ):
        super().__init__(name)
        self.type = typ
        self.constraint = []
        if isinstance(self.type, UjsBase):
            self.default_to_ujo = self.type.default_to_ujo
            self.typeid = self.type.typeid

        if isinstance(self.type, (UjsList, list)):

            def guess_default_type(val):
                types = self.type.type if isinstance(self.type, UjsList) else self.type
                for typ in types:
                    try:
                        return typ.default_to_ujo(val)
                    except (TypeError, ValueError):
                        pass
                raise ValueError(f"No matching type found for default: {val!r}")

            self.default_to_ujo = guess_default_type

    def __repr__(self):
        s = self.name + "=" + repr(self.type) + "::" + repr(self.constraint)
        if self.doc:
            s = s + "::doc '" + self.doc + "'"
        return s
