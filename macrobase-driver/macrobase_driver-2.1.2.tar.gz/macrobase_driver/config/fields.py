from typing import Type

from .base import BaseConfig, Field, CustomField
import ast


class Int(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, value) -> int:
        if value is None:
            return self._default

        return self.parse_value(value)

    @staticmethod
    def parse_value(value) -> int:
        return int(str(value))


class Float(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, value) -> float:
        if value is None:
            return self._default

        return self.parse_value(value)

    @staticmethod
    def parse_value(value) -> float:
        return float(str(value))


class Str(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, value) -> str:
        if value is None:
            return self._default

        return self.parse_value(value)

    @staticmethod
    def parse_value(value) -> str:
        return str(value)


class Bool(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, value) -> bool:
        if value is None:
            return self._default

        return self.parse_value(value)

    @staticmethod
    def parse_value(value) -> bool:
        return str(value).lower() in ('true', 'y', 'yes', '1', 'on')


class List(Field):

    def __init__(self, item_cls: Type[Field], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._item_cls = item_cls

    @property
    def item_cls(self) -> Type[Field]:
        return self._item_cls

    def parse(self, value) -> list:
        if value is None:
            return self._default

        result = self.parse_value(value)

        for i, v in enumerate(result):
            if value is None:
                raise Exception

            result[i] = self._item_cls.parse_value(v)

        return result

    @staticmethod
    def parse_value(value) -> list:
        if isinstance(value, list):
            return value
        elif isinstance(value, str):
            return ast.literal_eval(value)
        else:
            raise Exception



class Dict(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, value) -> dict:
        if value is None:
            return self._default

        return self.parse_value(value)

    @staticmethod
    def parse_value(value) -> dict:
        return dict(value)


class Nested(Field):

    def __init__(self, object_cls: Type[BaseConfig], *args, **kwargs):
        super().__init__(default=None, *args, **kwargs)
        self._object_cls = object_cls

    @property
    def default(self) -> BaseConfig:
        return self.object_cls()

    @property
    def object_cls(self) -> Type[BaseConfig]:
        return self._object_cls

    def parse(self, value) -> BaseConfig:
        if value is None:
            return self._default

        return self.object_cls(values=value)


class Custom(Field):

    def __init__(self, field_cls: Type[CustomField], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._field_cls = field_cls

    @property
    def field_cls(self) -> Type[CustomField]:
        return self._field_cls

    def parse(self, value) -> CustomField:
        if value is None:
            return self._default

        return self._field_cls.serialize(value=value)
