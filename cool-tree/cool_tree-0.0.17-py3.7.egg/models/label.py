import json
from spb.orm.type import Type
from spb.orm import Model
from spb.orm import AttributeModel
from spb.orm import ListAttribute
from spb.orm.type import String, ID, Number, Object, JsonObject


class Stats(AttributeModel, ListAttribute):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.count = kwargs['count'] if 'count' in kwargs else None


class Label(Model):
    RESOURCE_NAME = 'labels'

    # id
    id = ID(property_name='id', immutable=True, filterable=True)
    project_id = ID(property_name='projectId', filterable=True)

    # basic info
    status = String(property_name='status', immutable=True)
    stats = Object(property_name='stats', immutable=True, express=Stats)

    # For assets
    dataset = String(property_name='dataset')
    data_key = String(property_name='dataKey')

    # label datas
    result = JsonObject(property_name='result')

    @staticmethod
    def json_to_label(data: str = '{}'):
        result = json.loads(data)
        return Label(result)
