from collections.abc import MutableMapping

from .parser import UjsParser
from .transformer import UjsTransformer
from .converter import schema_to_markdown, schema_to_binary


def schema_from_str(schema_str):
    """
    create UJOSchema type definitions from a string representation

    parameter:
        schema_str: [string] a schema definition string

    return:
        [dictionary] type definition objects identified by names
    """
    return UjsSchema.from_str(schema_str)


class UjsSchema(MutableMapping):
    def __init__(self, schema: dict):
        self._schema = schema

    def __getitem__(self, key):
        return self._schema[key]

    def __setitem__(self, key, value):
        self._schema[key] = value

    def __delitem__(self, key):
        del self._schema[key]

    def __iter__(self):
        return iter(self._schema)

    def __len__(self):
        return len(self._schema)

    def __repr__(self):
        return self._schema.__repr__()

    @classmethod
    def from_str(cls, schema_str: str):
        parser = UjsParser(start="begin")
        parse_tree = parser.parse_string(schema_str)

        transformer = UjsTransformer()
        schema = transformer.transform(parse_tree)

        return cls(schema)

    def to_markdown(self):
        schema_to_markdown(self._schema)

    def to_ujo_binary(self):
        schema_to_binary(self._schema)
