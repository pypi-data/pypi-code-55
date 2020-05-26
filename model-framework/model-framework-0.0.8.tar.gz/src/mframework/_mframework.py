#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the Model-Framework authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Model framework
===============

.. code::

    |   User space   |       Specification
    |   ----------   |       -------------
    |                |
    |     Model      |  <---   ModelSpec
    |       |        |             |
    |       |        |             |
    |    Feature     | (<---) FeatureSpec
    |       |        |
    |       |        |
    |  (Properties)  |
"""

# TODO
# * 'required' should accept a positive int indicating how many instances are needed
# * Add check of required features/properties in 'run()' method
# * Add tests
#   - Result object
#   - ...

from abc import abstractmethod, ABCMeta
from collections.abc import MutableMapping
from uuid import uuid4

from schemadict import schemadict, STANDARD_VALIDATORS

from ._log import logger

PRIMITIVE_TYPES = (bool, int, float, str, dict, list, tuple)


def is_primitve_type(obj):
    return obj in PRIMITIVE_TYPES


def check_type(var_name, var, exp_type):
    if not isinstance(var, exp_type):
        raise TypeError(
            f"invalid type for {var_name!r}: expected {exp_type}, got {type(var)}"
        )


SchemadictValidators = STANDARD_VALIDATORS


class DictLike(MutableMapping):
    """
    Dictionary-like object.

    * Keys must be strings.
    """

    def __init__(self, *args, **kwargs):
        self.mapping = {}
        self.update(*args, **kwargs)

    def __str__(self):
        return f"{self.mapping!r}"

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.mapping!r})"

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"invalid key {key!r}: must be of type {str}, not {type(key)}")

        self.mapping[key] = value

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        del self.mapping[key]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)


class SpecDict(DictLike):
    """
    Specification dictionary.

    * Specification entries can only be defined once.
    """

    def __setitem__(self, key, value):
        if key in self.mapping.keys():
            raise KeyError(f"key {key!r}: entry already defined")
        if not isinstance(value, SpecEntry):
            raise ValueError(f"key {key!r}: value must be instance of 'SpecEntry'")
        super().__setitem__(key, value)


class ItemDict(DictLike):
    """
    Item dictionary.

    * Similar to a 'defaultdict(list)'
    """

    # TODO: keep reference of parent spec in ItemDict ?

    def __getitem__(self, key):
        if key not in self.mapping.keys():
            self.__missing__(key)
        return self.mapping[key]

    def __missing__(self, key):
        self.mapping[key] = list()


class SpecEntry:
    """
    Specification entry.
    """

    def __init__(self, schema, singleton=True, required=False, doc=''):
        self.schema = schema
        self.singleton = singleton
        self.required = required
        self.doc = doc

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema

    @property
    def singleton(self):
        return self._singleton

    @singleton.setter
    def singleton(self, singleton):
        check_type('singleton', singleton, bool)
        self._singleton = singleton

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, required):
        check_type('required', required, bool)
        self._required = required

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        check_type('doc', doc, str)
        self._doc = doc


class _BaseSpec:
    """
    Base class to store a collection of item specifications.

    The term 'item' may refer to a property (e.g. the number 5) if this class
    describes a feature, or it may also refer to a feature itself if this class
    describes a model.
    """

    def __init__(self):
        """
        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """

        self.uid = str(uuid4())
        self._specs = SpecDict()

    @property
    def keys(self):
        """Return all spec keys"""
        return self._specs.keys()

    def __repr__(self):
        return f"<Specification for {tuple(self._specs.keys())!r}>"

    def _add_item_spec(self, key, schema, *, singleton=True, required=False, doc=''):
        """
        Add a specification entry

        Args:
            :key: (str) name of item to specify
            :schema: (obj) specification
            :singleton: (bool) if True, make item singleton
            :required: (bool) if True, make item required
            :doc: (str) documentation

        Note:
            * 'schema' should be a primitive type or a 'schemadict' if a this
               class describes a feature. It should be an instance of
               'FeatureSpec' if this class describes a model.
            * When calling from subclass, add a user input check for 'schema'
        """

        self._specs[key] = SpecEntry(schema, singleton, required, doc)

    def _provide_user_class_from_base(self, base):
        """
        Return a user space class which subclasses from 'base'

        Args:
            :base: (obj) base class

        Returns:
            :UserSpace: (obj) user space class with specification reference
        """

        class UserSpace(base):
            _parent_specs = self._specs
            _parent_uid = self.uid

        return UserSpace

    def get_docs(self):
        """
        Return user documentation

        Returns:
            :docs: (dict) full documentation
        """

        docs = {}
        for key, spec in self._specs.items():
            subdocs = None
            if isinstance(getattr(spec, 'schema', None), _BaseSpec):
                subdocs = spec.schema.get_docs()

            docs[key] = {
                'main': self._specs[key].doc,
                'schema': self._specs[key].schema,
                'sub': subdocs,
                'singleton': self._specs[key].singleton,
                'required': self._specs[key].required,
            }

        return docs


class _UserSpaceBase:
    """
    Base class for user space functionality for 'model' or 'feature'.
    """

    _level = '$NONE'
    _parent_specs = None
    _parent_uid = None

    def __init__(self):
        """
        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """
        self.uid = str(uuid4())
        self._items = ItemDict()

    def __repr__(self):
        return f"<User space for {tuple(self._parent_specs.keys())!r}>"

    @property
    def keys(self):
        """Return all item keys"""
        return self._items.keys()

    def from_dict(self, d):
        """
        Add user values from a dictionary

        Args:
            :d: (dict) key-value pairs

        Returns:
            :self: (obj) reference to self
        """

        check_type(f'{d!r}', d, dict)

        for key, value in d.items():
            if key.startswith('$'):
                continue
            self._check_key_in_spec(key)
            if self._parent_specs[key].singleton:
                self.set(key, value[0])
            else:
                self.add(key, *value)
        return self

    def to_dict(self):
        """
        Represent model/feature as a dictionary

        Returns:
            :dictionary: (dict) key-value pairs
        """

        return {
            '$level': self._level,
            '$uid': self.uid,
            **dict(self._items)
        }

    def get_default(self, key):
        """
        Return the model/feature default values
        """

        raise NotImplementedError

    def set(self, key, value):
        """
        Set a value (singleton)

        Args:
            :key: (str) name of item to specify
            :value: (obj) value of the item to specify
        """

        self._check_key_in_spec(key)
        self._check_against_schema(key, value)

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"key {key!r}: method 'set()' does not apply, try 'add()'")

        logger.debug(f"Set property {key!r} = {value!r} in {self!r}")
        self._items[key] = [value, ]

    def add(self, key, *values):
        """
        Add a value (non-singleton)

        Args:
            :key: (str) name of item to specify
            :value: (obj) value of the item to specify
        """

        self._check_key_in_spec(key)

        for value in values:
            self._check_against_schema(key, value)

            if self._parent_specs[key].singleton:
                raise RuntimeError(f"key {key!r}: method 'add()' does not apply, try 'set()'")

            logger.debug(f"Add property {key!r} = {value!r} (num: {len(self._items[key])+1}) in {self!r}")
            self._items[key].append(value)

    def get(self, key):
        """
        Return a value (singleton/non-singleton)

        Args:
            :key: (str) name of item

        Returns:
            :value: (obj) value of the item
        """

        if self._parent_specs[key].singleton:
            return self._items[key][0]
        else:
            return self._items[key]

    def iter(self, key):
        """
        Return an iterator for values of 'key' (non-singleton)

        Args:
            :key: (str) name of item
        """

        if self._parent_specs[key].singleton:
            raise KeyError(f"Method 'iter()' not supported for item {key!r}, try 'get()'")

        yield from self._items[key]

    def len(self, key):
        return len(self._items[key])

    def _check_key_in_spec(self, key):
        if key not in self._parent_specs.keys():
            raise KeyError(f"key {key!r} is not in specification")

    def _check_against_schema(self, key, value):
        if isinstance(self._parent_specs[key].schema, dict):
            if not isinstance(value, dict):
                schemadict(
                    {f"{key}": self._parent_specs[key].schema},
                    validators=SchemadictValidators,
                ).validate({f"{key}": value})
            else:
                schemadict(
                    self._parent_specs[key].schema,
                    validators=SchemadictValidators
                ).validate(value)


class FeatureSpec(_BaseSpec):

    def add_prop_spec(self, key, schema, *, singleton=True, required=False, doc=''):
        """
        Add a property specification entry

        Args:
            :key: (str) name of property to specify
            :schema: (obj) specification (primitive type, or 'schemadict')
            :singleton: (bool) if True, make item singleton
            :required: (bool) if True, make item required
            :doc: (str) documentation
        """

        if not (is_primitve_type(schema) or isinstance(schema, dict)):
            raise TypeError(f"'schema' must be a primitive type or a 'schemadict'")

        # Always use a schemadict
        if is_primitve_type(schema):
            schema = {'type': schema}

        super()._add_item_spec(key, schema, singleton=singleton, required=required, doc=doc)

    @property
    def user_class(self):
        """Return a 'Feature' class with user and user methods"""
        return super()._provide_user_class_from_base(_FeatureUserSpace)


class _FeatureUserSpace(_UserSpaceBase):
    _level = '$feature'


class ModelSpec(_BaseSpec, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()

        # The model specification also includes a specification of the result
        # object which should be returned from the user space method 'run()'.
        # The result object must be an instance of this class.
        self._results = None

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        check_type('results', results, self.__class__)
        self._results = results

    def add_feature_spec(self, key, feature_spec, *, singleton=True, required=True, doc=''):
        """
        Add a feature specification entry

        Args:
            :key: (str) name of feature to specify
            :schema: (obj) specification (instance of FeatureSpec)
            :singleton: (bool) if True, make feature singleton
            :required: (bool) if True, make feature required
            :doc: (str) documentation
        """

        if not isinstance(feature_spec, FeatureSpec):
            raise TypeError(f"'feature_spec' must be instance of 'FeatureSpec'")

        super()._add_item_spec(key, feature_spec, singleton=singleton, required=required, doc=doc)

    @property
    def user_class(self):
        """Return a 'Model' class with user and user methods"""

        class Model(_ModelUserSpace):
            # If the result user space is specified, pass it down to the model
            # user space
            _result_user_class = getattr(self.results, 'user_class', None)

        return super()._provide_user_class_from_base(Model)


class _ModelUserSpace(_UserSpaceBase, metaclass=ABCMeta):
    _level = '$model'
    _result_user_class = None  # Specification of the result object

    def __init__(self):
        super().__init__()
        self.results = None

    def from_dict(self, dictionary):
        """
        Add user values from a dictionary

        Args:
            :dictionary: (dict) key-value pairs

        Returns:
            :self: (obj) reference to self
        """

        for key, fdicts in dictionary.items():
            if key.startswith('$'):
                continue

            self._check_key_in_spec(key)

            for fdict in fdicts:
                if self._parent_specs[key].singleton:
                    feature = self.set_feature(key)
                else:
                    feature = self.add_feature(key)
                feature.from_dict(fdict)
        return self

    def to_dict(self):
        """
        Represent model as a dictionary

        Returns:
            :dictionary: (dict) key-value pairs
        """

        model_dict = {
            '$level': self._level,
            '$uid': self.uid,
        }
        for key, features in self._items.items():
            model_dict[key] = []
            for feature in features:
                model_dict[key].append(feature.to_dict())
        return model_dict

    def set(self, key, _):
        return NotImplementedError

    def add(self, key, _):
        return NotImplementedError

    def set_feature(self, key):
        """
        Make a singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"key {key!r}: method 'set_feature()' does not apply, try 'add_feature()'")

        logger.debug(f"Set feature {key!r} in {self!r}")
        f_instance = self._parent_specs[key].schema.user_class()
        self._items[key] = [f_instance, ]  # Store instance as list of length 1
        return f_instance

    def add_feature(self, key):
        """
        Add a non-singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"key {key!r}: method 'add_feature()' does not apply, try 'set_feature()'")

        logger.debug(f"Add feature {key!r} (num: {len(self._items[key]) + 1}) in {self!r}")
        f_instance = self._parent_specs[key].schema.user_class()
        self._items[key].append(f_instance)
        return f_instance

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        The 'run()' method is the main entry point for evaluating the user
        model. This method needs to be overridden in the subclass. The 'run()'
        method should return an instance of '_result_user_class'. When
        implementing 'run()' in the subclass, the superclass 'run()' method
        should first be called with 'super().run()'.
        """

        # Instantiate the RESULT user if defined
        if self._result_user_class is not None:
            class Results(self._result_user_class):
                def run(self):
                    raise NotImplementedError
            self.results = Results()

        # TODO: check required features, properties...
