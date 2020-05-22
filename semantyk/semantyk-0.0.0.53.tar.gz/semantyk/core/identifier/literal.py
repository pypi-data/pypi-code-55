# -*- coding: utf-8 -*-
"""
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# Literal
Module | `literal.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"""

__all__ = ['Literal']

from ..namespace import RDF, XSD, OWL
from .identifier import Identifier
from .uriref import URIRef

class Literal(Identifier):
    _all_dtypes = (
        OWL.rational,
        RDF.HTMLLiteral,
        RDF.XMLLiteral,
        XSD.boolean,
        XSD.byte,
        XSD.decimal,
        XSD.double,
        XSD.float,
        XSD.int,
        XSD.integer,
        XSD.long,
        XSD.negativeInteger,
        XSD.nonNegativeInteger,
        XSD.nonPositiveInteger,
        XSD.normalizedString,
        XSD.positiveInteger,
        XSD.short,
        XSD.string,
        XSD.token,
        XSD.unsignedByte,
        XSD.unsignedInt,
        XSD.unsignedLong,
        XSD.unsignedShort
    )

    _number_dtypes = (
        XSD.byte,
        XSD.decimal,
        XSD.double,
        XSD.float,
        XSD.int,
        XSD.integer,
        XSD.long,
        XSD.negativeInteger,
        XSD.nonNegativeInteger,
        XSD.nonPositiveInteger,
        XSD.positiveInteger,
        XSD.short,
        XSD.unsignedByte,
        XSD.unsignedInt,
        XSD.unsignedLong,
        XSD.unsignedShort
    )

    _plain_dtypes = (
        OWL.rational,
        XSD.boolean,
        XSD.decimal,
        XSD.double,
        XSD.integer
    )

    _string_dtypes = (
        RDF.HTMLLiteral,
        RDF.XMLLiteral,
        XSD.normalizedString,
        XSD.string,
        XSD.token
    )

    @property
    def datatype(self):
        return self._datatype

    @property
    def language(self):
        return self._language

    @property
    def value(self):
        return self._value

    @staticmethod
    def is_valid_language(value):
        return bool(compile('^[a-zA-Z]+(?:-[a-zA-Z0-9]+)*$').match(value))

    def __abs__(self):
        if isinstance(self.value, (int, float)):
            return Literal(self.value.__abs__())
        else:
            raise TypeError("Not a number; %s" % repr(self))

    def __bool__(self):
        if self.value:
            return bool(self.value)
        return len(self) != 0

    def __invert__(self):
        if isinstance(self.value, (int, float)):
            return Literal(self.value.__invert__())
        else:
            raise TypeError("Not a number; %s" % repr(self))

    def __getstate__(self):
        return (None, dict(language=self.language, datatype=self.datatype))

    def __neg__(self):
        if isinstance(self.value, (int, float)):
            return Literal(self.value.__neg__())
        else:
            raise TypeError("Not a number; %s" % repr(self))

    def __new__(cls, value, language=None, datatype=None):
        literal = str.__new__(cls, value)
        literal._language = language
        literal._datatype = datatype
        return literal


    def __pos__(self):
        if isinstance(self.value, (int, float)):
            return Literal(self.value.__pos__())
        else:
            raise TypeError("Not a number; %s" % repr(self))

    def __reduce__(self):
        return (Literal, (str(self), self.language, self.datatype),)