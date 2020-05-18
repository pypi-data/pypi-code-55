from marshmallow import Schema, fields, post_load
from splitiorequests.schemas.splits.split_definition_schema import SplitDefinitionSchema
from splitiorequests.models.splits.split_definitions import SplitDefinitions


class SplitDefinitionsSchema(Schema):
    objects = fields.List(fields.Nested(SplitDefinitionSchema), required=True)
    offset = fields.Int(required=True)
    limit = fields.Int(required=True)
    totalCount = fields.Int(required=True)

    @post_load
    def load_split_definitions(self, data, **kwargs):
        return SplitDefinitions(**data)
