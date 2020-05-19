# (C) Michael DeHaan <michaeldehaan.net>, 2020

import base64

DEFAULT_SENTINEL = '__no_default__'

class Field(object):

    __slots__ = [
        'name',
        'type',
        'default',
        'nullable',
        'mutable',
        'accessor',
        'mutator',
        '_mutated',
        'choices',
        'value',
        'required',
        'remap',
        'hidden',
        'encode',
        'decode'
    ]

    def __init__(self, name=None, type=None, default=DEFAULT_SENTINEL, nullable=True, mutable=None, mutator=None, accessor=None,
                 choices=None, required=False, hidden=False, remap=None, encode=None, decode=None):

        assert mutator is None or (isinstance(mutator, str))
        assert accessor is None or (isinstance(accessor, str))

        self.type = type
        self.default = default
        self.nullable = nullable
        self.mutable = mutable
        self.mutator = mutator
        self._mutated = False
        self.accessor = accessor
        self.choices = choices
        self.value = None
        self.required = required
        self.hidden = hidden
        self.remap = remap
        self.encode = encode
        self.decode = decode

        if default != DEFAULT_SENTINEL and self.value is None:
            self.value = default

    def _has_default(self):
        return self.default != DEFAULT_SENTINEL

    def _show(self):

        return dict(
            type = self.type,
            default = self.default,
            nullable = self.nullable,
            mutable = self.mutable,
            mutator = self.mutator,
            accessor = self.accessor,
            choices = self.choices,
            value = self.value,
            required = self.required,
            remap = self.remap,
            hidden = self.hidden,
            encode = self.encode,
            decode = self.decode
        )

    def copy(self):
        obj = self.__class__(type=self.type, default=self.default, nullable=self.nullable, mutable=self.mutable,
                    mutator=self.mutator, accessor=self.accessor, choices=self.choices, required=self.required,
                    remap=self.remap, hidden=self.hidden, encode=self.encode, decode=self.decode)
        obj._mutated = False
        obj.value = self.value
        return obj

    def _INTERNAL_get(self, parent, name):
        # return the value of the field
        return self._find_function(parent, self.accessor, self.field_access, "get_%s" % name)(self.value)

    def _INTERNAL_serialize(self, parent, name, value, remap_name):
        return self._find_function(parent, self.encode, self.field_encode, "encode_%s" % name)(value, remap_name)

    def _INTERNAL_deserialize(self, parent, name, value, remap_name):
        return self._find_function(parent, self.decode, self.field_decode, "decode_%s" % name)(value, remap_name)

    def _INTERNAL_set(self, parent, name, value, from_init=False):

        if not from_init:
            self._mutated = True

        if not self.mutable and self._mutated:
            raise ValueError("field is immutable: %s" % name)


        if value is None and not self.nullable:
            raise ValueError("field is not nullable: %s" % name)

        if (self.nullable and value is not None) and (self.type is not None) and not isinstance(value, self.type):
            raise ValueError("invalid field type for %s. got %s, expected: %s" % (name, value, self.type))

        if self.choices is not None and not value in self.choices:
            raise ValueError("rejected value for %s: choices=%s" % (name, self.choices))

        fn = self._find_function(parent, self.mutator, self.field_mutate, "set_%s" % name)
        self.value = fn(value)

    def _find_function(self, parent, member, default_func, func_pattern):
        if member is None:
            # no named mutator function was passed into the field, so...
            fn2 = getattr(parent, func_pattern, None)
            if fn2 is not None:
                # use a funciton named get/set_<fieldname> if available...
                return fn2
        else:
            # a named member function was specified, so use if available, or error
            fn3 = getattr(parent, member, None)
            if fn3 is None:
                raise AttributeError("missing function: %s" % member)
            return fn3
        return default_func

# =======
# methods below this line are safe to subclass:

    def field_access(self, value):
        # optionally could override this in a subclass
        return value

    def field_mutate(self, value):
        # optionally could override this in a subclass
        return value

    def field_encode(self, value, remap_name):
        if hasattr(value, 'to_dict'):
            return value.to_dict()
        return value

    def field_decode(self, value, remap_name):
        if hasattr(self.type, 'from_dict'):
            return self.type.from_dict(value)
        else:
            return value

# ======================================================================================================================
# BEGIN STANDARD LIBRARY OF FIELDS
# ======================================================================================================================

class Base64(Field):

    """
    Base64 field is just a string that encodes as base64 during serialization.
    """

    def __init__(self, **kwargs):
        kwargs['type'] = str
        super(Base64, self).__init__(**kwargs)

    def field_encode(self, value, remap_name=None):
        return base64.b64encode(bytes(value, 'utf-8'))

    def field_decode(self, value, remap_name=None):
        return str(base64.b64decode(value), 'ascii')

# ======================================================================================================================

class Numeric(Field):

    __slots__ = [ '_type', 'places', 'min', 'max', 'fold', 'inclusive' ]

    def __init__(self, type=None, inclusive=True, places=None, min=None, max=None, fold=None,
                 default=DEFAULT_SENTINEL, required=False, hidden=False, remap=None):

        self._type = type
        self.places = places

        if self._type is None and self.places is None or self.places == 0:
            self._type = int

        self.inclusive = inclusive
        self.min = min
        self.max = max
        self.fold = fold

        Field.__init__(self, type=None, default=default, nullable=False, required=required, hidden=hidden, remap=remap)

    def _show(self):
        data = super(Numeric, self)._show()
        data.update(dict(
            inclusive = self.inclusive,
            places = self.places,
            min = self.min,
            max = self.max,
            fold = self.fold,
        ))
        return data

    def copy(self):
        
        # FIXME: make this easier to subclass
        obj = self.__class__(type=self._type, inclusive=self.inclusive, places=self.places, min=self.min, max=self.max, fold=self.fold,
                             default=self.default, required=self.required, hidden=self.hidden, remap=self.remap)
        obj._mutated = False
        obj.value = self.value
        return obj

    def field_mutate(self, value):

        v2  = value

        if self.places is not None:
            v2 = round(value, self.places)
        elif self._type == int:
            try:
                v2 = int(v2)
            except:
                raise ValueError("an integer is expected")

        if self.inclusive:
            if self.max is not None and v2 > self.max:
                if not self.fold:
                    raise ValueError("value: %s exceeds max: %s" % (value, self.max))
                else:
                    v2 = self.max
            if self.min is not None and v2 < self.min:
                if not self.fold:
                    raise ValueError("value: %s below min: %s" % (value, self.min))
                else:
                    v2 = self.min
        else:
            if self.max is not None and v2 >= self.max:
                if not self.fold:
                    raise ValueError("value: %s exceeds max: %s" % (value, self.max))
                else:
                    v2 = self.max
            if self.min is not None and v2 <= self.min:
                if not self.fold:
                    raise ValueError("value: %s below min: %s" % (value, self.min))
                else:
                    v2 = self.min

        return v2

