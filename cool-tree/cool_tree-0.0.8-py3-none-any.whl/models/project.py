import json

from spb.orm.type import Type
from spb.orm import Model
from spb.orm import AttributeModel

class Class(AttributeModel):
    def __init__(self, *args, **kwargs ):
        self.name = kwargs['name'] if 'name' in kwargs else None
        self.annotationType = kwargs['annotationType'] if 'annotationType' in kwargs else None
        self.properties = kwargs['properties'] if 'properties' in kwargs else None


class Configure(AttributeModel):
    def __init__(self, *args, **kwargs):
        self.dataType = kwargs['dataType'] if 'dataType' in kwargs else None
        self.annotationTypes = kwargs['annotationTypes'] if 'annotationTypes' in kwargs else None
        self.classList = [Class(**item) for item in kwargs['classList']] if 'classList' in kwargs else None


class Project(Model):
    RESOURCE_NAME = 'projects'

    id = Type(property_name='id', immutable=True, filterable=True)
    name = Type(property_name='name')
    label_count = Type(property_name='labelCount')
    configure = Type(property_name='configure', express=Configure)
