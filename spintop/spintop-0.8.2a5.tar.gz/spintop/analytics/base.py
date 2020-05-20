from copy import deepcopy
import json
from contextlib import contextmanager

from spintop.models.serialization import get_json_serializer
from ..logs import _logger

logger = _logger('singer')

class AbstractSingerTarget(object):
    def __init__(self):
        self.serializer = get_json_serializer()
    
    @contextmanager
    def stream(self, stream_name):
        batch = CollectMessagesFromFactory(stream_name)
        yield batch
        self.send_messages(self.json_dumps_messages(batch.messages))

    def json_dumps_messages(self, messages):
        serialized_messages = [self.serializer.serialize(msg) for msg in messages]
        return [json.dumps(ser_msg) for ser_msg in serialized_messages]

    def send_messages(self, messages_str):
        raise NotImplementedError()

class CollectMessagesFromFactory(object):
    def __init__(self, stream_name):
        self.messages = []
        self.factory = SingerMessagesFactory(stream_name)

    def __getattr__(self, key):
        factory_fn = getattr(self.factory, key)
        def _wrapper(*args, **kwargs):
            self.messages.append(factory_fn(*args, **kwargs))
        return _wrapper

class SingerMessagesFactory(object):
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.logger = logger.getChild(stream_name)

    def schema(self, schema , key_properties):
        schema = deepcopy(schema)
        _schema_transform(schema)
        return {
            'type': 'SCHEMA',
            'stream': self.stream_name,
            'key_properties': key_properties,
            'schema': schema
        }

    def record(self, data):
        return {
            'type': 'RECORD',
            'stream': self.stream_name,
            'record': data
        }


### Replace datetime by string type.
_FIELD_TRANSFORM = {
    'datetime': lambda field: {'type': 'string', 'format': 'date-time'}
}

def _schema_transform(schema):
    try:
        fields = schema.get('properties', {})
    except AttributeError:
        return 
    
    for key, field in fields.items():
        # Try to get type in map, else keep same.
        # Also add null allowed everywhere.
        transformer = _FIELD_TRANSFORM.get(field['type'], None)
        if transformer:
            update = transformer(field)
            field.update(update)

        field['type'] = [field['type'], 'null']

        # in case it contains other properties (object)
        _schema_transform(field)