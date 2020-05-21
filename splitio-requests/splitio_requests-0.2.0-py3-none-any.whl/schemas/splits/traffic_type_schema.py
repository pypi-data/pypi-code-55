from marshmallow import Schema, fields, post_load
from splitiorequests.models.splits.traffic_type import TrafficType


class TrafficTypeSchema(Schema):
    traffic_id = fields.Str(required=True, data_key='id')
    name = fields.Str(required=True)

    @post_load
    def load_traffic_type(self, data, **kwargs):
        return TrafficType(**data)
