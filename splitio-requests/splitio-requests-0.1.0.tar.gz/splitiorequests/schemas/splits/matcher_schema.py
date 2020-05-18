from marshmallow import Schema, fields, post_dump, post_load
from splitiorequests.schemas.splits import between_schema, depends_schema
from splitiorequests.models.splits.matcher import Matcher


class MatcherSchema(Schema):
    matcher_type = fields.Str(required=True, data_key='type')
    string = fields.Str()
    negate = fields.Bool()
    depends = fields.Nested(depends_schema.DependsSchema)
    attribute = fields.Str()
    strings = fields.List(fields.Str())
    date = fields.Int()
    between = fields.Nested(between_schema.BetweenSchema)
    number = fields.Int()
    bool = fields.Bool()

    @post_load
    def load_matcher(self, data, **kwargs):
        return Matcher(**data)

    @post_dump
    def clean_empty(self, data, **kwargs):
        new_data = data.copy()
        for field_key in (key for key in data if data[key] is None):
            del new_data[field_key]
        return new_data
