from .base_datatype_mapper import BaseDatatypeMapper

class SetMapperDecorator(BaseDatatypeMapper):
    def __init__(self, mapper):
        self.mapper = mapper
        self.condition_type = self.mapper.datatype.condition_type + "S"

    def resolve(self, value):
        return [self.mapper.resolve(i) for i in value]

    def parse(self, value):
        return [self.mapper.parse(i) for i in value]
