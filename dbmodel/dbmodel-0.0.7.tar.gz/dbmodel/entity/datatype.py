# -*- coding: utf-8 -*-

import decimal

import datetime

from dbmodel.entity.status import EntityStatus


class ValidateValue:

    def __init__(self, pk=False, auto_increment=False, fk=False, not_null=False, required=False, max=None, name=None, type=None, format=None, precision=None, scale=None, key=None, reference=None, table=None, intermediate=None, inter_key=None, end_key=None):
        self.pk = pk
        self.fk = fk
        self.required = required
        self.max = max
        self.name = name
        self.type = type
        self.auto_increment = auto_increment
        self.not_null = not_null
        self.precision = precision
        self.scale = scale
        self.format = format
        self.key = key
        self.reference = reference
        self.table = table
        self.intermediate = intermediate
        self.inter_key = inter_key
        self.end_key = end_key

    def __call__(self, obj, **kw):
        self.func = obj
        self.field_name = obj.__name__[
            1:] if obj.__name__.startswith("_") else obj.__name__
        return self

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class String(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if not isinstance(data, str):
                raise Exception("%s requires string" % self.field_name)
            if self.max and len(data) > self.max:
                raise Exception("Value too large. The default limit for %s field is %s" % (
                    self.field_name, self.max))
        super().__setattr__(attr, data)


class Int(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if self.max and len(str(data)) > self.max:
                raise Exception("Value too large. The default limit for %s field is %s" % (
                    self.field_name, self.max))
            if not isinstance(data, int):
                try:
                    data = int(data)
                except ValueError as e:
                    raise Exception("%s requires int" % self.field_name)
        super().__setattr__(attr, data)


class DateTime(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if not isinstance(data, datetime.datetime):
                try:
                    data = datetime.datetime.strptime(data, self.format)
                except ValueError as e:
                    if "unconverted data remain" not in str(e):
                        raise Exception("%s requires datetime" %
                                        self.field_name)
                    pass
        super().__setattr__(attr, data)


class Decimal(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if not isinstance(data, Decimal):
                try:
                    data = decimal.Decimal(str(round(float(data), self.scale)))
                except ValueError as e:
                    raise Exception("%s requires Decimal" % self.field_name)
        super().__setattr__(attr, data)


class Float(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if not isinstance(data, float):
                try:
                    data = round(float(data), self.scale)
                except ValueError as e:
                    raise Exception("%s requires Float" % self.field_name)
        super().__setattr__(attr, data)


class Boolean(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if not isinstance(data, bool):
                try:
                    data = bool(data)
                except ValueError as e:
                    raise Exception("%s requires Boolean" % self.field_name)
        super().__setattr__(attr, data)


class Dict(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if not isinstance(data, dict):
                raise Exception("%s requires Dict" % self.field_name)
        super().__setattr__(attr, data)


class Object(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            if data.__class__.__name__ != self.type.__name__:
                raise Exception("%s requires %s object" %
                                (self.field_name, self.type.__name__))
        super().__setattr__(attr, data)


class ObjectList(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            raise Exception(
                "method not allowed, please use `%s.append(Object)`" % self.field_name)
        super().__setattr__(attr, data)


class ObjectManyList(ValidateValue):

    def __init__(self, **attrs):
        super().__init__(**attrs)

    def __setattr__(self, attr, data):
        if attr == "value" and data is not None:
            raise Exception(
                "method not allowed, please use `%s.append(Object)`" % self.field_name)
        super().__setattr__(attr, data)


class ListType(list):

    def __init__(self, context, type):
        try:
            self._type = type
            self.__context__ = context
            super(ListType, self).__init__()
        except Exception as e:
            raise e

    def append(self, item):
        try:
            if item.__class__.__name__ != self._type.__name__:
                raise Exception('Item type not is %s' % self._type.__name__)
            super(ListType, self).append(item)
            if self.__context__:
                if "__status__" in self.__context__.__dict__:
                    if self.__context__.__status__ == EntityStatus.created or self.__context__.__status__ == EntityStatus.filled:
                        self.__context__.__status__ = EntityStatus.addedobject
                    self.__context__.__commit__.append(item)
        except Exception as e:
            raise e

    def add(self, item):
        self.append(item)

    def toJSON(self):
        try:
            return [item.toJSON() if hasattr(item, "toJSON") else item for item in self]
        except Exception as e:
            raise e

    def orderby(self, field):
        try:
            if len(self) > 1:
                _field, _order = field.strip(), "ASC"
                if " " in _field:
                    _field, _order = _field.split(" ")[0], _field.split(" ")[1]
                _reverse = _order == "DESC"
                self.sort(key=lambda x: x.__getattribute__(
                    _field), reverse=_reverse)
            return self
        except Exception as e:
            raise e

    def where(self, condition):
        try:
            itens = filter(condition, self)
            new_list = ListType(context=self.__context__, type=self._type)
            for item in itens:
                new_list.append(item)
            return new_list
        except Exception as e:
            raise e

    @property
    def first(self):
        try:
            if len(self) > 0:
                return self[0]
            else:
                return None
        except Exception as e:
            raise e

    @property
    def last(self):
        try:
            if len(self) > 0:
                return self[-1]
            else:
                return None
        except Exception as e:
            raise e

    @property
    def count(self):
        try:
            return len(self)
        except Exception as e:
            raise e
