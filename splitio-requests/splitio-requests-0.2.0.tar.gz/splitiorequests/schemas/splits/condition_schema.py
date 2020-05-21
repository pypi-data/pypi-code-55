from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.condition import Condition
from splitiorequests.schemas.splits.matcher_schema import MatcherSchema


class ConditionSchema(Schema):
    combiner = fields.Str(required=True)
    matchers = fields.List(fields.Nested(MatcherSchema), required=True)

    @post_load
    def load_condition(self, data, **kwargs):
        return Condition(**data)
