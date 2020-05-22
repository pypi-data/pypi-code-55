# -*- coding: utf-8 -*-
"""
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# URIRef
Module | `uriref.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"""

__all__ = ['URIRef']

import logging

from .identifier import Identifier

_logger = logging.getLogger(__name__)

class URIRef(Identifier):
    _invalid_chars = '<>" {}|\\^`'

    def is_valid(self):
        return all(map(lambda c: ord(c) > 256 or not c in _invalid_chars, self))

    def toPython(self):
        return str(self)

    def __add__(self, other):
        return self.__class__(str(self) + other)

    def __getnewargs__(self):
        return (str(self), )

    def __mod__(self, other):
        return self.__class__(str(self) % other)

    def __new__(cls, value):
        if not is_valid(value):
            _logger.warning('%s does not look like a valid URI, trying to serialize this will break.' % value)
        return str.__new__(cls, value)

    def __radd__(self, other):
        return self.__class__(other + str(self))

    def __reduce__(self):
        return (URIRef, (str(self),))

    def __repr__(self):
        if self.__class__ is URIRef:
            cls_name = 'semantyk.core.identifier.uriref.URIRef'
        else:
            cls_name = self.__class__.__name__
        return "%s(%s)" % (cls_name, super(URIRef, self).__repr__())
