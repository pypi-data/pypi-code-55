import yaml
import jsonschema
import argparse
import pathlib
import os
from jsonschema_cli.load import load_file, load_string
from jsonschema_cli.handlers import handle_file_uri
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
        data_path = None
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

    parser.add_argument(
        "schema_file_or_string", type=str, help="The schema you want to use to validate the data",
    )
    parser.add_argument(
        "data_file_or_string", type=str, help="The data you want validated by the schema",
    )
    parser.add_argument(
        "-r, --resolver", type=str, help="A list of files to load for $ref to resolve too", choices=[""],
    )

    return parser


def default_handler():
    raise NotImplementedError("Handler not defined for URI schema")


def main(args):
    path, schema = load_schema(args.schema_file_or_string)
    instance = load_instance(args.data_file_or_string)

    handler = default_handler
    if path is not None:
        handler = handle_file_uri(path)

    ref_handlers = {"": handler, "file": handler}
    resolver = jsonschema.RefResolver("", {}, handlers=ref_handlers)

    jsonschema.Draft7Validator(schema, resolver=resolver).validate(instance=instance)
