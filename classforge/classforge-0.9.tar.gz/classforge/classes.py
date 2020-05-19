
# (C) Michael DeHaan <michaeldehaan.net>, 2020

from classforge.fields import Field
import json
import yaml

class Class(object):

    __SLOTS__ = [ '_cf_fields' ]

    def __init__(self, *args, **kwargs):

        self._cf_fields = {}

        # shadow class variables with instance variables
        supers = self.__class__.mro()
        for super in supers:
            members = super.__dict__.keys()
            for attribute in members:
                value = super.__dict__[attribute]
                if attribute not in self._cf_fields:
                    if isinstance(value, Field):
                        f = value.copy()
                        if self.is_strict():
                            self._enforce_strict(attribute, f)
                        else:
                            self._non_strict(f)
                        self._cf_fields[attribute] = f

        # check for required parameters
        if '_no_check' not in kwargs:
            for (k,v) in self._cf_fields.items():
                if v.required and k not in kwargs:
                    raise AttributeError("%s is required" % k)

        # apply key value arguments to values
        for (k,v) in kwargs.items():
            if k != '_no_check':
                self._cf_fields[k]._INTERNAL_set(self, k, v, from_init=True)

        # call init hooks
        supers = reversed(self.__class__.mro())
        for super in supers:
            init_fn = getattr(super, 'on_init', None)
            if init_fn:
                init_fn(self)

    def explain(self):
        result = dict()
        for (name, field) in self._cf_fields.items():
            result[name] = field._show()
        return result

    def _enforce_strict(self, name, field):
        if field.mutable is None:
            field.mutable = False
        if not field._has_default():
            field.required = True
        if field.type is None:
            raise AttributeError("type for %s is required" % name)

    def _non_strict(self, field):
        if field.mutable is None:
            field.mutable = True

    def is_strict(self):
        return False

    def on_init(self):
        pass

    def __setattr__(self, what, value):

        # allow direct access to instance variables
        if what in Class.__SLOTS__:
            object.__setattr__(self, what, value)
            return

        # field lookups for anything else
        field = self._cf_fields.get(what)
        field._INTERNAL_set(self, what, value)

    def __getattribute__(self, what):
        # lookup fields through special code, otherwise don't for other variables
        fields = super(Class, self).__getattribute__('_cf_fields')
        if what in fields:
            return fields[what]._INTERNAL_get(self, what)
        return super(Class, self).__getattribute__(what)

    def _get_remap_key(self, key, remap_name):

        # support for remapped serialization (see docs)
        field = self._cf_fields[key]
        if field.remap is None:
            return key
        elif isinstance(field.remap, str):
            return field.remap
        elif isinstance(field.remap, dict):
            if remap_name in field.remap:
                return field.remap[remap_name]
            else:
                return key
        else:
            raise RuntimeError("invalid remap specification for field: %s" % key)

    def _get_reversed_remap_key(self, key, remap_name):

        for (k,v) in self._cf_fields.items():
            if v.remap is not None:
                if type(v.remap) == str and v.remap == key:
                    return k
                elif type(v.remap) == dict:
                    if remap_name in v.remap:
                        if v.remap[remap_name] is None:
                            return None
                        elif v.remap[remap_name] == key:
                            return k
                    elif k == key:
                        return k
            elif k == key:
                return k
        return None

    def to_dict(self, remap_name=None):

        # dump the class variables to a dict, recursively
        data = dict()
        for (k,v) in self._cf_fields.items():
            if v.hidden:
                continue
            k2 = self._get_remap_key(k, remap_name)
            if k2 is None:
                continue
            data[k2] = v._INTERNAL_serialize(self, k, v.value, remap_name=remap_name)
        return data

    @classmethod
    def from_dict(cls, values, remap_name=None):

        # load the class variables from a dict, also recursively
        placeholder = cls(_no_check=True)
        new_dict = dict()
        for (k,v) in values.items():
            k2 = placeholder._get_reversed_remap_key(k, remap_name)
            if k2 is None:
                continue
            field = getattr(cls, k2)
            new_dict[k2] = field._INTERNAL_deserialize(placeholder, k2, v, remap_name=remap_name)
        return cls(**new_dict)

    def to_yaml(self, remap_name=None, **kwargs):
        return yaml.dump(self.to_dict(remap_name=remap_name), **kwargs)

    @classmethod
    def from_yaml(cls, values, remap_name=None, **kwargs):
        return cls.from_dict(yaml.safe_load(values, **kwargs), remap_name=remap_name)

    def to_json(self, remap_name=None, **kwargs):
        return json.dumps(self.to_dict(remap_name=remap_name), **kwargs)

    @classmethod
    def from_json(cls, values, remap_name=None, **kwargs):
        return cls.from_dict(json.loads(values, **kwargs), remap_name=remap_name)

class StrictClass(Class):

    def is_strict(self):
        return True