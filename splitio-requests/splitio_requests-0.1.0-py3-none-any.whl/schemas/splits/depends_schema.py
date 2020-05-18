from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.depends import Depends


class DependsSchema(Schema):
    splitName = fields.Str(required=True)
    treatments = fields.List(fields.Str(), required=True)

    @post_load
    def load_depends(self, data, **kwargs):
        return Depends(**data)
