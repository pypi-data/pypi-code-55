from splitiorequests.schemas.splits.split_schema import SplitSchema
from splitiorequests.models.splits.split import Split
from splitiorequests.schemas.splits.split_definition_schema import SplitDefinitionSchema
from splitiorequests.models.splits.split_definition import SplitDefinition
from splitiorequests.models.splits.split_definitions import SplitDefinitions
from splitiorequests.schemas.splits.split_definitions_schema import SplitDefinitionsSchema
from splitiorequests.common.utils import Utils


def load_split(data: dict, unknown_handler: str = 'RAISE') -> Split:
    handler = Utils.get_unknown_field_handler(unknown_handler)
    loaded_split = SplitSchema(unknown=handler).load(data)
    return loaded_split


def dump_split(split_obj: Split) -> dict:
    dumped_split = SplitSchema().dump(split_obj)
    return dumped_split


def load_split_definition(data: dict, unknown_handler: str = 'RAISE') -> SplitDefinition:
    handler = Utils.get_unknown_field_handler(unknown_handler)
    loaded_split_definition = SplitDefinitionSchema(unknown=handler).load(data)
    return loaded_split_definition


def dump_split_definition(split_definition_obj: SplitDefinition) -> dict:
    dumped_split_definition = SplitDefinitionSchema().dump(split_definition_obj)
    return dumped_split_definition


def load_split_definitions(data: dict, unknown_handler: str = 'RAISE') -> SplitDefinitions:
    handler = Utils.get_unknown_field_handler(unknown_handler)
    loaded_split_definitions = SplitDefinitionsSchema(unknown=handler).load(data)
    return loaded_split_definitions


def dump_split_definitions(split_definitions_obj: SplitDefinitions) -> dict:
    dumped_split_definitions = SplitDefinitionsSchema().dump(split_definitions_obj)
    return dumped_split_definitions
