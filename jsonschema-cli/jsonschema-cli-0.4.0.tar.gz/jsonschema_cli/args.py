import yaml
import jsonschema
import argparse
import pathlib
import os
from jsonschema_cli.load import load_file, load_string
from jsonschema_cli.resolvers import relative_path_resolver
import enum
import json
import yaml


class JsonschemaException(Exception):
    def __str__(self):
        return " ".join(self.args)


def load_schema(schema: str) -> dict:
    data_path = pathlib.Path(schema).absolute()

    if os.path.isfile(data_path):
        loaded_data = load_file(data_path)

        if type(loaded_data) is not dict:
            raise JsonschemaException(f'Schema file must be a a map, cannot load file: "{schema}"')
    else:
        data_path = pathlib.Path(os.getcwd()).absolute()
        loaded_data = load_string(schema)

        if type(loaded_data) is not dict:
            raise JsonschemaException(f'JSON/YAML string must be a a map, cannot load "{schema}"')

    return data_path, loaded_data


def load_instance(data: str) -> dict:
    data_path = pathlib.Path(data).absolute()

    if os.path.isfile(data_path):
        loaded_data = load_file(data_path)
    else:
        loaded_data = load_string(data)
        if not loaded_data:
            raise JsonschemaException("Instance data cannot be empty")

    return loaded_data


def create_parser():
    parser = argparse.ArgumentParser(
        "jsonschema-cli",
        description="A wrapper around https://github.com/Julian/jsonschema to validate JSON using the CLI",
    )

    validate_parser = parser.add_subparsers(help='Validate thet json data with a schema').add_parser('validate', help='Validate')

    validate_parser.add_argument(
        "schema_file_or_string", type=str, help="The schema you want to use to validate the data against",
    )
    validate_parser.add_argument(
        "data_file_or_string", type=str, help="The data you want validated by the schema",
    )

    validate_parser.set_defaults(func=schema_validate)

    return parser





def schema_validate(args):
    path, schema = load_schema(args.schema_file_or_string)
    instance = load_instance(args.data_file_or_string)

    jsonschema.Draft7Validator(schema, resolver=relative_path_resolver(path)).validate(instance=instance)
