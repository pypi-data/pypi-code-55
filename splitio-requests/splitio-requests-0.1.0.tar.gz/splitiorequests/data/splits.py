from splitiorequests.schemas.splits.split_schema import SplitSchema
from splitiorequests.models.splits.split import Split
from splitiorequests.schemas.splits.split_definition_schema import SplitDefinitionSchema
from splitiorequests.models.splits.split_definition import SplitDefinition
from splitiorequests.models.splits.split_definitions import SplitDefinitions
from splitiorequests.schemas.splits.split_definitions_schema import SplitDefinitionsSchema


def load_split(data: dict) -> Split:
    loaded_split = SplitSchema().load(data)
    return loaded_split


def dump_split(split_obj: Split) -> dict:
    dumped_split = SplitSchema().dump(split_obj)
    return dumped_split


def load_split_definition(data: dict) -> SplitDefinition:
    loaded_split_definition = SplitDefinitionSchema().load(data)
    return loaded_split_definition


def dump_split_definition(split_definition_obj: SplitDefinition) -> dict:
    dumped_split_definition = SplitDefinitionSchema().dump(split_definition_obj)
    return dumped_split_definition


def load_split_definitions(data: dict) -> SplitDefinitions:
    loaded_split_definitions = SplitDefinitionsSchema().load(data)
    return loaded_split_definitions


def dump_split_definitions(split_definitions_obj: SplitDefinitions) -> dict:
    dumped_split_definitions = SplitDefinitionsSchema().dump(split_definitions_obj)
    return dumped_split_definitions
