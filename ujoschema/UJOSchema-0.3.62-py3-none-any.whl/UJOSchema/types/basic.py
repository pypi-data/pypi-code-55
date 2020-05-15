#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" basic types """

from ujotypes import (
    UjoInt8,
    UjoInt16,
    UjoInt32,
    UjoInt64,
    UjoUInt8,
    UjoUInt16,
    UjoUInt32,
    UjoUInt64,
    UjoFloat16,
    UjoFloat32,
    UjoFloat64,
    UjoStringUTF8,
    UjoStringC,
    UjoBool,
    UjoTimestamp,
    UJO_VARIANT_NONE,
)


def undefined_ujo_type(*args, **kwargs):  # pylint: disable=unused-argument
    return UJO_VARIANT_NONE


class UjsBase:
    name = "abstract class UjsTypeAtomic"
    typeid = 0xFF
    default_to_ujo = undefined_ujo_type

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class UjsInt8(UjsBase):
    name = "int8"
    typeid = 0x08
    default_to_ujo = UjoInt8


class UjsInt16(UjsBase):
    name = "int16"
    typeid = 0x07
    default_to_ujo = UjoInt16


class UjsInt32(UjsBase):
    name = "int32"
    typeid = 0x06
    default_to_ujo = UjoInt32


class UjsInt64(UjsBase):
    name = "int64"
    typeid = 0x05
    default_to_ujo = UjoInt64


class UjsUInt8(UjsBase):
    name = "uint8"
    typeid = 0x0C
    default_to_ujo = UjoUInt8


class UjsUInt16(UjsBase):
    name = "uint16"
    typeid = 0x0B
    default_to_ujo = UjoUInt16


class UjsUInt32(UjsBase):
    name = "uint32"
    typeid = 0x0A
    default_to_ujo = UjoUInt32


class UjsUint64(UjsBase):
    name = "uint64"
    typeid = 0x09
    default_to_ujo = UjoUInt64


class UjsFloat16(UjsBase):
    name = "float16"
    typeid = 0x03
    default_to_ujo = UjoFloat16


class UjsFloat32(UjsBase):
    name = "float32"
    typeid = 0x02
    default_to_ujo = UjoFloat32


class UjsFloat64(UjsBase):
    name = "float64"
    typeid = 0x01
    default_to_ujo = UjoFloat64


class UjsUtf8String(UjsBase):
    name = "string"
    typeid = 0x04
    default_to_ujo = UjoStringUTF8


class UjsCString(UjsBase):
    name = "cstring"
    typeid = 0x04
    default_to_ujo = UjoStringC


class UjsBinary(UjsBase):
    name = "binary"
    typeid = 0x0D
    default_to_ujo = undefined_ujo_type  # UjoBinary ??


class UjsBool(UjsBase):
    name = "bool"
    typeid = 0x0E
    default_to_ujo = UjoBool


class UjsDateTime(UjsBase):
    name = "datetime"
    typeid = 0x10
    default_to_ujo = undefined_ujo_type  # UjoDateTime?


class UjsDate(UjsBase):
    name = "date"
    typeid = 0x11
    default_to_ujo = undefined_ujo_type  # UjoDate?


class UjsTime(UjsBase):
    name = "time"
    typeid = 0x12
    default_to_ujo = undefined_ujo_type  # UjoDate?


class UjsTimestamp(UjsBase):
    name = "timestamp"
    typeid = 0x13
    default_to_ujo = UjoTimestamp


class UjsVariant(UjsBase):
    typeid = 0xAA
    name = "variant"
    default_to_ujo = undefined_ujo_type


# custom type
class CustomType(UjsBase):
    def __init__(self, name):
        self.name = name
