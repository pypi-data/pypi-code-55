from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.bucket import Bucket


class BucketSchema(Schema):
    treatment = fields.Str(required=True)
    size = fields.Int(required=True)

    @post_load
    def load_bucket(self, data, **kwargs):
        return Bucket(**data)
