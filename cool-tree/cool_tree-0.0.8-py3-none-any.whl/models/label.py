import json
from spb.orm.type import Type
from spb.orm import Model
from spb.orm import AttributeModel
from spb.orm import ListAttribute


class LabelObject(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.id = kwargs['id'] if 'id' in kwargs else None
        self.klass = kwargs['klass'] if 'klass' in kwargs else None
        self.shape = kwargs['shape'] if 'shape' in kwargs else None
        self.propertices = kwargs['properties'] if 'properties' in kwargs else None


class LabelResult(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.objects = [LabelObject(**item) for item in kwargs['objects']] if 'objects' in kwargs else None


class Stats(AttributeModel, ListAttribute):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.count = kwargs['count'] if 'count' in kwargs else None


class Label(Model):
    RESOURCE_NAME = 'labels'

    # id
    id = Type(property_name='id', immutable=True, filterable=True)
    project_id = Type(property_name='projectId', filterable=True)

    # basic info
    status = Type(property_name='status')
    stats = Type(property_name='stats', express=Stats)

    # For assets
    dataset = Type(property_name='dataset')
    data_key = Type(property_name='dataKey')

    # label datas
    result = Type(property_name='result', express=LabelResult)

    @staticmethod
    def json_to_label(data: str = '{}'):
        result = json.loads(data)
        return Label(result)
