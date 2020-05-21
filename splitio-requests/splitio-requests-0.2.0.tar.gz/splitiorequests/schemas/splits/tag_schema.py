from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.tag import Tag


class TagSchema(Schema):
    name = fields.Str(required=True)

    @post_load
    def load_tag(self, data, **kwargs):
        return Tag(**data)
