from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.default_rule import DefaultRule


class DefaultRuleSchema(Schema):
    treatment = fields.Str(required=True)
    size = fields.Int(required=True)

    @post_load
    def load_default_rule(self, data, **kwargs):
        return DefaultRule(**data)
