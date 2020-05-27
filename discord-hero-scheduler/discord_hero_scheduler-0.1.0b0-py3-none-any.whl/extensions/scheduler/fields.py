import json

from hero import fields


class JSONField(fields.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', {})
        kwargs.setdefault('max_length', 65536)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value or value == '{}':
            return {}
        if isinstance(value, dict):
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if not value:
            return '{}'
        return json.dumps(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
