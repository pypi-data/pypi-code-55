from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.between import Between


class BetweenSchema(Schema):
    from_number = fields.Int(data_key='from', required=True)
    to = fields.Int(required=True)

    @post_load
    def load_between(self, data, **kwargs):
        return Between(**data)
