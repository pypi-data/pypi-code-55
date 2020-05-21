from marshmallow import Schema, fields, post_load
from splitiorequests.schemas.splits import bucket_schema, condition_schema
from splitiorequests.models.splits.rule import Rule


class RuleSchema(Schema):
    buckets = fields.List(fields.Nested(bucket_schema.BucketSchema), required=True)
    condition = fields.Nested(condition_schema.ConditionSchema, required=True)

    @post_load
    def load_rule(self, data, **kwargs):
        return Rule(**data)
