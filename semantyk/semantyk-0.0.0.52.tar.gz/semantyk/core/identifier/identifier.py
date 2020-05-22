# -*- coding: utf-8 -*-
"""
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Identifier
Module | `identifier.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"""

__all__ = ['Identifier']

from collections import defaultdict
from ..node import Node

class Identifier(Node, str):
    _order = defaultdict(int)
    _order.update({'BNode': 1, 'Variable': 2, 'URIRef': 3, 'Literal': 4})

    __hash__ = str.__hash__

    def __eq__(self, other):
        if type(self) == type(other):
            return str(self) == str(other)
        return False

    def __ge__(self, other):
        if self.__gt__(other):
            return True
        return self == other

    def __gt__(self, other):
        if other is None:
            return True
        elif type(self) == type(other):
            return str(self) > str(other)
        elif isinstance(other, Node):
            self_class = str(type(self).__name__)
            other_class = str(type(other).__name__)
            return _order[self_class] > _order[other_class]
        return NotImplemented

    def __le__(self, other):
        if self.__lt__(other):
            return True
        return self == other

    def __lt__(self, other):
        if other is None:
            return False
        elif type(self) == type(other):
            return str(self) < str(other)
        elif isinstance(other, Node):
            self_class = str(type(self).__name__)
            other_class = str(type(other).__name__)
            return _order[self_class] < _order[other_class]
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __new__(cls, value):
        return str.__new__(cls, value)
