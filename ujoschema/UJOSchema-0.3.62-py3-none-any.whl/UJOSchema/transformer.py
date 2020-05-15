#
# Copyright (c) 2018-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" transforming the parsed AST """

import logging

from lark import Transformer

from .ranges import UjsWord, UjsAbove, UjsBetween, UjsBelow, UjsEquals
from .constraints import UjsNotNull, UjsConstraint, UjsOfLength, UjsIn, UjsContains, UjsNotIn
from .types import (
    UjsInt8,
    UjsInt16,
    UjsInt32,
    UjsInt64,
    UjsUInt8,
    UjsUInt16,
    UjsUInt32,
    UjsUint64,
    UjsFloat16,
    UjsFloat32,
    UjsFloat64,
    UjsUtf8String,
    UjsCString,
    UjsBinary,
    UjsBool,
    UjsDate,
    UjsTime,
    UjsDateTime,
    UjsTimestamp,
    UjsVariant,
    UjsList,
    UjsMap,
    Typedef,
    Module,
    CustomType,
    Object,
    ObjectItem,
    Record,
    RecordItem,
)

log = logging.getLogger(__name__)


# transformer
class UjsTransformer(Transformer):
    # pylint: disable=no-self-use, unused-argument, too-many-public-methods

    def __init__(self):
        super().__init__(self)
        self.parse_tree = None

    def not_null(self, matches):
        log.debug("not null")
        log.debug(matches)
        result = UjsNotNull()
        if matches:
            result.default = matches[0]
        return result

    def default(self, matches):
        log.debug("default")
        log.debug(matches)
        return matches[0]

    def documentation(self, matches):
        # log.debug("doc")
        # log.debug(matches)

        if matches[0].type == "LONG_STRING":
            return matches[0].value[3:-3]
        if matches[0].type == "STRING":
            return matches[0].value[1:-1]

        raise Exception("invalid documentation string type")

    def int8(self, matches):
        return UjsInt8()

    def int16(self, matches):
        return UjsInt16()

    def int32(self, matches):
        return UjsInt32()

    def int64(self, matches):
        return UjsInt64()

    def uint8(self, matches):
        return UjsUInt8()

    def uint16(self, matches):
        return UjsUInt16()

    def uint32(self, matches):
        return UjsUInt32()

    def uint64(self, matches):
        return UjsUint64()

    def float16(self, matches):
        return UjsFloat16()

    def float32(self, matches):
        return UjsFloat32()

    def float64(self, matches):
        return UjsFloat64()

    def utf8string(self, matches):
        return UjsUtf8String()

    def string(self, matches):
        return UjsUtf8String()

    def cstring(self, matches):
        return UjsCString()

    def binary(self, matches):
        return UjsBinary()

    def bool(self, matches):
        return UjsBool()

    def date(self, matches):
        return UjsDate()

    def time(self, matches):
        return UjsTime()

    def datetime(self, matches):
        return UjsDateTime()

    def timestamp(self, matches):
        return UjsTimestamp()

    def list(self, matches):
        log.debug("list")
        log.debug(matches)
        return UjsList(matches[0])

    def variant(self, matches):
        return UjsVariant()

    def identifier(self, matches):
        log.debug("identifier")
        log.debug(matches)
        return matches[0].value

    def of_length(self, matches):
        log.debug("of_length")
        log.debug(matches)

        return UjsOfLength(matches[0])

    def primitive_type(self, matches):
        log.debug("primitive_type")
        log.debug(matches)

        result = Typedef(matches[0], matches[1])
        for element in matches[2:]:
            if isinstance(element, UjsConstraint):
                result.constraint.append(element)

        # documentation found
        if isinstance(matches[-1], str):
            result.doc = matches[-1]

        del matches[2:]
        return (matches[0], result)

    def custom_type(self, matches):
        log.debug("custom_type")
        log.debug(matches)

        return CustomType(matches[0].value)

    def value(self, matches):
        # log.debug("value")
        # log.debug(matches)
        try:
            number = int(matches[0].value)
        except ValueError:
            number = float(matches[0].value)
        return number

    def words(self, matches):
        # log.debug("words")
        # log.debug(matches)

        return matches

    def word(self, matches):
        # log.debug("word")
        # log.debug(matches)

        if len(matches) > 1:
            return UjsWord(matches[0], matches[1])

        return UjsWord(matches[0])

    def chars(self, matches):
        # log.debug("chars")
        # log.debug(matches)

        return matches[0].value[1:-1]

    def value_set(self, matches):
        log.debug("value_set")
        log.debug(matches)

        if isinstance(matches[0], list):
            return UjsIn(matches[0])

        return UjsIn(matches)

    def not_in(self, matches):
        log.debug("value_set")
        log.debug(matches)

        return UjsNotIn(matches[0])

    def range(self, matches):
        log.debug("range")
        log.debug(matches)

        return matches

    def above(self, matches):
        # log.debug("above")
        # log.debug(matches)

        if len(matches) > 1:
            return UjsAbove(matches[0], matches[1])

        return UjsAbove(matches[0])

    def between(self, matches):
        # log.debug("between")
        # log.debug(matches)

        if len(matches) == 3:
            # documentation found
            return UjsBetween(matches[0], matches[1], matches[2])

        return UjsBetween(matches[0], matches[1])

    def below(self, matches):
        # log.debug("below")
        # log.debug(matches)

        if len(matches) > 1:
            return UjsBelow(matches[0], matches[1])

        return UjsBelow(matches[0])

    def equals(self, matches):
        log.debug("equals")
        log.debug(matches)

        if len(matches) > 1:
            return UjsEquals(matches[0], matches[1])

        return UjsEquals(matches[0])

    def contains(self, matches):
        log.debug("contains")
        log.debug(matches)

        return UjsContains(matches)

    def item(self, matches):
        log.debug("item")
        log.debug(matches)

        result = RecordItem(matches[0], matches[1])
        for element in matches[2:]:
            if isinstance(element, UjsConstraint):
                result.constraint.append(element)

        # documentation found
        if isinstance(matches[-1], str):
            result.doc = matches[-1]

        return result

    def record(self, matches):
        log.debug("record")
        log.debug(matches)

        result = Record(matches[0])

        for element in matches[1:]:
            if isinstance(element, RecordItem):
                result.items.append(element)
            elif isinstance(element, CustomType):
                result.extends = element

        # documentation found
        if isinstance(matches[-1], str):
            result.doc = matches[-1]

        return (matches[0], result)

    def object(self, matches):
        log.debug("object")
        log.debug(matches)

        result = Object(matches[0], matches[1], [])
        for element in matches[1:]:
            if isinstance(element, ObjectItem):
                result.items.append(element)
            elif isinstance(element, CustomType):
                result.extends = element

        # documentation found
        if isinstance(matches[-1], str):
            result.doc = matches[-1]

        return matches[0], result

    def object_item(self, matches):
        log.debug("object_item")
        log.debug(matches)

        typ = next((m for m in matches[1:] if not isinstance(m, str)), None)

        result = ObjectItem(str(matches[0]), typ)

        for element in matches:
            if isinstance(element, UjsConstraint):
                result.constraint.append(element)
            elif isinstance(element, str) and element == "*?*":
                result.optional = True
            elif isinstance(element, str):
                result.doc = element

        return result

    def optional(self, matches):
        log.debug("multi_type")
        log.debug(matches)

        return "*?*"

    def multi_type(self, matches):
        log.debug("multi_type")
        log.debug(matches)

        return matches

    def map_type(self, matches):
        log.debug("map_type")
        log.debug(matches)

        return UjsMap(tuple(matches))

    def extending(self, matches):
        log.debug("extending")
        log.debug(matches)

        return matches[0]

    def module(self, matches):
        log.debug("extending")
        log.debug(matches)

        result = Module(matches[0])

        if len(matches) > 1:
            result.doc = matches[1]

        return (matches[0], result)

    def begin(self, matches):
        log.debug("begin")
        log.debug(matches)

        return dict(matches)
