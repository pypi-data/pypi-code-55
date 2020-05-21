import cro_validate.classes.definition_classes as Definitions
import cro_validate.classes.util_classes as Utils
from cro_validate.enum import DataType


def get(definition_or_name):
	return Definitions.Index.get(definition_or_name)


def exists(name):
	return Definitions.Index.exists(name)


def as_dict():
	return Definitions.Index.as_dict()


def register_definition(
 			name=None,
			aliases=set(),
			description='',
			data_type=DataType.String,
			data_format=None,
			default_value=Utils.DataDefinitionDefaultValue(),
			examples=None,
			nullable=False,
			is_internal=False,
			rules=[],
			transforms=[],
			meta=None,
			dependency_resolver=None
		):
	if meta is None:
		meta = Definitions.DefaultMeta()
	if dependency_resolver is None:
		dependency_resolver = Definitions.DefaultResolver()
	result = Definitions.Index.register_definition(
			name=name,
			aliases=aliases,
			description=description,
			data_type=data_type,
			data_format=data_format,
			default_value=default_value,
			examples=examples,
			nullable=nullable,
			is_internal=is_internal,
			rules=rules,
			transforms=transforms,
			meta=meta,
			dependency_resolver=dependency_resolver
		)
	return result


def ensure_alias(name, alias):
	Definitions.Index.ensure_alias(name, alias)


def list_definitions():
	results = Definitions.Index.list_definitions()
	return results


def list_dependent_definitions(definition_name):
	results = Definitions.Index.list_dependent_definitions(definition_name)
	return results


def list_fields(name_or_definition):
	definition = name_or_definition
	if not isinstance(definition, Definitions.Definition):		
		definition = get(str(name_or_definition))
	if definition.data_type == DataType.Object:
		field_names = definition.validator.list_field_names()
		result = {
				k: {
						'definition_name': definition.validator.model_validator.get_field_definition_name(k),
						'input_name': definition.validator.model_validator.get_field_input_name(k),
						'input_display_name': definition.validator.model_validator.get_field_input_display_name(k),
					}
				for k in field_names
			}
		return result
	return {}


def validate_inputs(validated, **kw):
	results = Definitions.Index.validate_inputs(validated, **kw)
	return results


def validate_input(definition_or_name, value, validated=None, field_fqn=None, field_name=None, dependent_values={}):
	results = Definitions.Index.validate_input(validated, field_fqn, field_name, definition_or_name, value, dependent_values)
	return results