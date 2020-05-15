#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

"""
Range values with documentation used in constraints like `length` and `in`.
"""

from abc import ABC, abstractmethod


class UjsValueBase(ABC):
    def __init__(self, doc=None):
        self.doc = doc

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class UjsEquals(UjsValueBase):
    def __init__(self, value, doc=None):
        self.value = value
        super().__init__(doc)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        s = str(self.value) if (not self.doc) else str(self.value) + ":" + self.doc
        return s


class UjsBetween(UjsValueBase):
    def __init__(self, low, high, doc=None):
        super().__init__(doc)
        self.low = low
        self.high = high

    def __str__(self):
        return str(self.low) + " .. " + str(self.high)

    def __repr__(self):
        s = str(self.low) + " .. " + str(self.high)
        if self.doc:
            s = s + ":" + self.doc
        return s


class UjsAbove(UjsValueBase):
    def __init__(self, value, doc=None):
        super().__init__(doc)
        self.value = value

    def __str__(self):
        return ">=" + str(self.value)

    def __repr__(self):
        s = ">=" + str(self.value)
        if self.doc:
            s = s + ":" + self.doc
        return s


class UjsBelow(UjsValueBase):
    def __init__(self, value, doc=None):
        super().__init__(doc)
        self.value = value

    def __str__(self):
        return "<=" + str(self.value)

    def __repr__(self):
        s = "<=" + str(self.value)
        if self.doc:
            s = s + ":" + self.doc
        return s


class UjsWord(UjsValueBase):
    def __init__(self, value, doc=None):
        super().__init__(doc)
        self.value = value

    def __str__(self):
        return "'" + self.value + "'"

    def __repr__(self):
        s = "'" + self.value + "'"
        if self.doc:
            s = s + ":" + self.doc
        return s
