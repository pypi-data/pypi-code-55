# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Xml simple schema.
"""

import abc
from collections import abc as abccl

from ..helper import function as helperfun  # type: ignore
from ..xml import converter as c
from ..xml import io


class SchemaItem(c.Converter):
    """Metadata for every item in the schema.

    Args:
        path: something that converts to XmlPathElement list
        converter: xml data converter
        default: default data value

    """

    def __init__(self, path, converter=c.StringConverter, default=None):
        xpe_list = io.XmlPathElement.from_list(path)
        real_converter = (
            Schema(**converter) if isinstance(converter, dict) else converter
        )
        self.accessor = io.XmlAccessor(path=xpe_list, converter=real_converter)
        self.default = default

    def from_node(self, node):
        return self.accessor.read(node)

    def to_node(self, obj, node):
        data = self.default if obj is None else obj
        self.accessor.write(node, data)


class Schema(c.Converter, abccl.Mapping):  # pylint: disable=too-many-ancestors
    """Dict-like of schema items and its properties.

    Args:
        **kwargs(Dict[str, SchemaItem]): Schema items.

    """

    def __init__(self, **kwargs):
        self._subitems = {
            key: self._parse_attr(key, value) for key, value in kwargs.items()
        }

    @staticmethod
    def _parse_attr(key, value):
        if isinstance(value, SchemaItem):
            return value
        if isinstance(value, dict):
            if "path" not in value:
                return SchemaItem(path=helperfun.camelcase(key), **value)
            return SchemaItem(**value)
        raise Exception("Cannot convert to SchemaItem.")

    def from_node(self, node):
        return {
            key: attr.from_node(node) for key, attr in self._subitems.items()
        }

    def to_node(self, obj, node):
        for key, attr in self._subitems.items():
            if key in obj:
                attr.to_node(obj[key], node)

    def __getitem__(self, key):
        return self._subitems[key]

    def __len__(self):
        return len(self._subitems)

    def __iter__(self):
        return iter(self._subitems)


class CleanSetAttrMeta(abc.ABCMeta):
    """Metaclass that allows __setattr__ to take effect after initialization.

    From https://stackoverflow.com/q/16426141/86783

    """

    def __call__(cls, *args, **kwargs):  # noqa: N805 (failing for some reason)
        real_setattr = cls.__setattr__
        cls.__setattr__ = object.__setattr__
        self = super().__call__(*args, **kwargs)
        cls.__setattr__ = real_setattr
        return self


class SchemaData(abccl.MutableMapping, metaclass=CleanSetAttrMeta):
    """Dictionary with schema.

    This class implements a dictionary with an schema, so only items in the
    schema are allowed. It also allows to access the dictionary items as
    instance attributes.

    The schema allows for default values.

    """

    def __init__(self, schema, **kwargs):
        """Initializer.

        Args:
            schema (dict): An Schema instance.
            **kwargs: values to initialize the object.
        """
        self._schema = schema
        self._data = {}
        self.update(kwargs)

    def __getitem__(self, key):
        if key in self._schema:
            value = self._data.get(key, None)
            if value is None:
                # try default
                return self._schema[key].default
            return value
        raise KeyError(str(key))

    def __delitem__(self, key):
        if key in self._schema:
            self._data.pop(key, None)
        else:
            raise KeyError(str(key))

    def __setitem__(self, key, value):
        if key in self._schema:
            self._data[key] = value
        else:
            raise KeyError(str(key))

    def __iter__(self):
        return iter(self._schema)

    def __len__(self):
        return len(self._schema)

    def attr_str(self):
        "Return attribute/value string"
        return ", ".join(f"{key}={value}" for key, value in self.items())

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.attr_str())

    def __repr__(self):
        return f"{self.__class__.__name__}@{id(self):x}"

    def __getattr__(self, attr):
        # only called when other methods fail
        try:
            value = self[attr]
        except KeyError:
            raise AttributeError(attr)
        return value

    def __setattr__(self, attr, value):
        if attr in self._schema:
            self._data[attr] = value
        else:
            object.__setattr__(self, attr, value)
