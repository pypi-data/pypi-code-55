from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.environment import Environment


class EnvironmentSchema(Schema):
    environment_id = fields.Str(data_key='id', required=True)
    name = fields.Str(required=True)

    @post_load
    def load_environment(self, data, **kwargs):
        return Environment(**data)
