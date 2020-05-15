#
# Copyright (c) 2020-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" conversion of a schema to Ujo binary representation """
from abc import abstractmethod, ABC
from copy import deepcopy

from ujotypes import (
    UJO_VARIANT_NONE,
    UjoUInt8,
    UjoList,
    UjoStringUTF8,
    UjoUInt32,
    UjoMap,
    UjoBool,
)

from UJOSchema.types import (
    Module,
    Typedef,
    CustomType,
    UjsList,
    UjsMap,
    Object,
    Record,
    RecordItem,
)
from UJOSchema.constraints import UjsNotNull, UjsIn, UjsNotIn, UjsOfLength
from UJOSchema.ranges import UjsEquals, UjsBetween, UjsAbove, UjsWord, UjsBelow

from .base import (
    BaseSchemaConverter,
    BaseTypeConverter,
    BaseConstraintConverter,
    BaseRangeConverter,
)


def schema_to_binary(schema, target=None):
    return bytes(SchemaToUjo(schema).convert(target))


class SchemaToUjo(BaseSchemaConverter):
    def __init__(self, schema):
        super().__init__(schema)
        self.type_converter = TypeToUjoConverter(self.schema, None)
        self.convert_type = self.type_converter.convert_type

    def convert(self, target=None):  # pylint: disable=arguments-differ
        if target:
            return self.convert_type(self.schema[target])

        converted = [
            self.convert_type(typ)
            for typ in self.schema.values()
            if not isinstance(typ, Module)
        ]

        if len(converted) == 1:
            return next(iter(converted))

        results = UjoList()
        for typ in converted:
            results.append(typ)
        return results


class TypeToUjoConverter(BaseTypeConverter):
    @property
    def type_name(self):
        return UjoStringUTF8(self.typ.name)

    @property
    def type_id(self):
        return UjoUInt8(self.typ.typeid)

    def convert(self):
        pass

    def create_container(self):
        container = UjoList()
        container.append(self.type_name)
        container.append(self.type_id)
        return container

    def convert_type(self, typ):
        default_converter = BasicTypeToUjo
        converters = {
            list: ListOfTypesToUjo,
            tuple: ListOfTypesToUjo,
            Typedef: TypedefToUjo,
            UjsList: ContainerToUjo,
            UjsMap: ContainerToUjo,
            CustomType: CustomTypeToUjo,
            Record: RecordToUjo,
            RecordItem: TypedefToUjo,
            Object: ObjectToUjo,
        }

        converter = converters.get(type(typ)) or default_converter
        return converter(self.schema, typ).convert()


class BasicTypeToUjo(TypeToUjoConverter):
    def convert(self):
        return self.type_id


class ListOfTypesToUjo(TypeToUjoConverter):
    def convert(self):
        type_list = UjoList()
        for typ in self.typ:
            type_list.append(self.convert_type(typ))
        return type_list


class TypedefToUjo(TypeToUjoConverter):
    def resolve_custom_type(self):
        """ replace the current type with the referenced one,
            but keep current name & doc-string and merge any constraints """
        customtype = deepcopy(self.schema[self.typ.type.name])

        # keep original name & doc-string
        for attr in ("name", "doc"):
            setattr(customtype, attr, getattr(self.typ, attr))

        # merge constraints
        if any(hasattr(t, "constraint") for t in (customtype, self.typ)):
            setattr(customtype, "constraint", getattr(customtype, "constraint", []))
            customtype.constraint += getattr(self.typ, "constraint", [])

        self.typ = customtype

    def convert(self):
        if isinstance(self.typ.type, CustomType):
            self.resolve_custom_type()

        # resolving the CustomType may change our "Typdef"-typ into something else

        if isinstance(self.typ, (Record, Object)):
            container = self.convert_type(self.typ)
            container.set_value(0, self.type_name, "FixMe")
            # there can be no constraints here, so we can already return this
            return container

        if isinstance(self.typ.type, (UjsList, UjsMap)):
            container = self.convert_type(self.typ.type)
            container.set_value(0, self.type_name, "FixMe")
        else:
            container = UjoList()
            container.append(self.type_name)
            container.append(self.convert_type(self.typ.type))

        container.append(constraints_to_ujo(self.typ))
        return container


class ContainerToUjo(TypeToUjoConverter):
    def convert(self):
        container = self.create_container()
        container.append(self.convert_type(self.typ.type))
        return container


class RecordToUjo(TypeToUjoConverter):
    def convert(self):
        if getattr(self.typ, "extends"):
            container = self.convert_type(self.schema[self.typ.extends.name])
            container.set_value(0, self.type_name, "FIXME")
        else:
            container = self.create_container()
            container.append(UjoList())

        fields = container[-1]
        for item in self.typ:
            fields.append(self.convert_type(item))
        return container


class ObjectToUjo(TypeToUjoConverter):
    def convert(self):
        if isinstance(self.typ.type, CustomType):
            container = self.convert_type(self.typ.type)
            container.set_value(0, self.type_name, "FIXME")
        else:
            container = self.create_container()
            container.append(UjoMap())

        items = container[-1]
        for name, item in self.convert_items():
            items[name] = item

        return container

    def convert_items(self):
        for item in self.typ:
            yield UjoStringUTF8(item.name), self.convert_item(item)

    def convert_item(self, item):
        if isinstance(item.type, (UjsList, UjsMap, Record, Object, CustomType)):
            container = self.convert_type(item.type)
            container.pop(0)  # remove name
        else:
            container = UjoList()
            # "or self.typ.type[1]" to get the "value-type" defined for the object
            # in case the item itself was defined without any type
            container.append(self.convert_type(item.type or self.typ.type.type[1]))

        container.append(constraints_to_ujo(item))
        container.append(UjoBool(item.optional))
        return container


class CustomTypeToUjo(TypeToUjoConverter):
    def convert(self):
        return self.convert_type(self.schema[self.typ.name])


def constraints_to_ujo(type_instance):
    # constraints
    converters = {
        UjsNotNull: NotNullToUjo,
        UjsOfLength: LengthToUjo,
        UjsIn: InOrExcludeToUjo,
        UjsNotIn: InOrExcludeToUjo,
    }

    container = UjoList()
    for constraint in type_instance.constraint:
        converter = converters.get(type(constraint))
        container.append(converter(constraint, type_instance.default_to_ujo).convert())
    return container


class ConstraintToUjoConverter(BaseConstraintConverter, ABC):
    def __init__(self, constraint, ujo_default_factory):
        super().__init__(constraint)
        self.ujo_default_factory = ujo_default_factory

    def create_container(self):
        container = UjoList()
        container.append(UjoUInt8(self.constraint.typeid))
        return container

    def range_to_ujo(self, range_):
        return RangeToUjo(range_, self.ujo_default_factory).convert()

    @abstractmethod
    def convert(self):
        pass


class NotNullToUjo(ConstraintToUjoConverter):
    def convert(self):
        container = self.create_container()
        if self.constraint.default is not None:
            container.append(self.ujo_default_factory(self.constraint.default))
        else:
            container.append(UJO_VARIANT_NONE)
        return container


class LengthToUjo(ConstraintToUjoConverter):
    def convert(self):
        self.ujo_default_factory = UjoUInt32

        container = self.create_container()
        container.append(self.range_to_ujo(self.constraint.length))
        return container


class InOrExcludeToUjo(ConstraintToUjoConverter):
    def convert(self):
        container = self.create_container()
        values = UjoList()
        container.append(values)
        for value in self.constraint:
            values.append(self.range_to_ujo(value))
        return container


class RangeToUjo(BaseRangeConverter):
    def __init__(self, range_, ujo_default_factory):
        super().__init__(range_)
        self.ujo_default_factory = ujo_default_factory

    def convert(self):
        if isinstance(self.range, (UjsEquals, UjsWord)):
            return self.ujo_default_factory(self.range.value)

        container = UjoList()

        if isinstance(self.range, UjsBetween):
            container.append(self.ujo_default_factory(self.range.low))
            container.append(self.ujo_default_factory(self.range.high))

        elif isinstance(self.range, UjsAbove):
            container.append(self.ujo_default_factory(self.range.value))
            container.append(UJO_VARIANT_NONE)

        elif isinstance(self.range, UjsBelow):
            container.append(UJO_VARIANT_NONE)
            container.append(self.ujo_default_factory(self.range.value))

        return container
