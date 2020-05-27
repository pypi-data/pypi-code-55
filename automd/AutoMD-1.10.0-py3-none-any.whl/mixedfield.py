from typing import Iterable, Dict, Any

from marshmallow import ValidationError, fields
from marshmallow.fields import Field


class MixedField(Field):
    def __init__(self, field_types: Iterable[Field], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_types: Iterable[Field] = field_types

    def _serialize(self, value, attr, obj, **kwargs):
        result: Any = None
        found_type: bool = False

        for field_type in self.field_types:
            try:
                result = field_type._serialize(value, attr, obj, **kwargs)
                found_type = True
                break
            except Exception:
                # could not parse, trying next field_type
                pass
        if not found_type:
            message: str = (f"Value {value} could not be serialized by Mixed Field using"
                            f" types {[type(field).__name__ for field in self.field_types]}")
            raise ValidationError(message)
        return result

    def _deserialize(self, value, attr, data, **kwargs):
        result: Any = None
        found_type: bool = False

        for field_type in self.field_types:
            try:
                result = field_type._deserialize(value, attr, data, **kwargs)
                found_type = True
                break
            except Exception:
                # could not parse, trying next field_type
                pass
        if not found_type:
            message: str = (f"Value {value} could not be deserialized by Mixed Field using"
                            f" types {[type(field).__name__ for field in self.field_types]}")
            raise ValidationError(message)
        return result


# Based on implementation from
# https://github.com/marshmallow-code/apispec/issues/471
def mixedfield_2properties(self, field: fields.Field, ret: Dict, **kwargs):
    if isinstance(field, MixedField):
        ret.pop('type', None)
        ret['oneOf'] = [self.field2property(f) for f in field.field_types]
    return ret
