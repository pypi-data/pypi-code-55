import json
from unittest import mock
from pytest_mock import MockFixture

import pytest
import yaml

from jsonschema_cli.main import JsonschemaException, create_parser, main
import jsonschema


@pytest.fixture
def success_arguments():
    schema = {"properties": {"number": {"type": "integer"}}, "required": ["number"]}
    instance = {"number": 123}

    return schema, instance


@pytest.fixture
def fail_validation_arguments():
    schema = {
        "properties": {"number": {"type": "integer"}, "fail_on_required": {"type": "any"}},
        "required": ["number", "fail_on_required"],
    }
    instance = {"number": 123}

    return schema, instance


def test_load_json_string(success_arguments):
    schema, instance = success_arguments

    args = create_parser().parse_args([json.dumps(schema), json.dumps(instance)])
    main(args)


def test_load_yaml_string(success_arguments):
    schema, instance = success_arguments

    args = create_parser().parse_args([yaml.dump(schema), yaml.dump(instance)])
    main(args)


def test_load_yaml_schema_json_instance(success_arguments):
    schema, instance = success_arguments

    args = create_parser().parse_args([yaml.dump(schema), json.dumps(instance)])
    main(args)


def test_load_json_schema_yaml_instance(success_arguments):
    schema, instance = success_arguments

    args = create_parser().parse_args([json.dumps(schema), yaml.dump(instance)])
    main(args)


@pytest.mark.xfail(raises=jsonschema.ValidationError)
def test_failed_load_json_string(fail_validation_arguments):
    schema, instance = fail_validation_arguments

    args = create_parser().parse_args([json.dumps(schema), json.dumps(instance)])
    main(args)


@pytest.mark.xfail(raises=jsonschema.ValidationError)
def test_failed_load_yaml_string(fail_validation_arguments):
    schema, instance = fail_validation_arguments

    args = create_parser().parse_args([yaml.dump(schema), yaml.dump(instance)])
    main(args)


@pytest.mark.xfail(raises=jsonschema.ValidationError)
def test_failed_load_yaml_schema_json_instance(fail_validation_arguments):
    schema, instance = fail_validation_arguments

    args = create_parser().parse_args([yaml.dump(schema), json.dumps(instance)])
    main(args)


@pytest.mark.xfail(raises=jsonschema.ValidationError)
def test_failed_load_json_schema_yaml_instance(fail_validation_arguments):
    schema, instance = fail_validation_arguments

    args = create_parser().parse_args([json.dumps(schema), yaml.dump(instance)])
    main(args)


@pytest.mark.xfail(raises=JsonschemaException)
def test_load_empty_instance_fails(success_arguments):
    schema, instance = success_arguments

    args = create_parser().parse_args([json.dumps(schema), ""])
    main(args)

def test_load_json_schema_file(mocker: MockFixture, success_arguments: tuple):
    schema, instance = success_arguments

    mock_isfile = mocker.patch('os.path.isfile')
    mock_isfile.side_effect = lambda x: x.name == "schema.json"

    mock_load_file = mocker.patch('jsonschema_cli.main.load_file', mocker.MagicMock(return_value=schema))
    args = create_parser().parse_args(["schema.json", json.dumps(instance)])
    main(args)

def test_load_yaml_schema_file(mocker: MockFixture, success_arguments: tuple):
    schema, instance = success_arguments

    mock_isfile = mocker.patch('os.path.isfile')
    mock_isfile.side_effect = lambda x: x.name == "schema.yaml"

    mock_load_file = mocker.patch('jsonschema_cli.main.load_file', mocker.MagicMock(return_value=schema))
    args = create_parser().parse_args(["schema.yaml", yaml.dump(instance)])
    main(args)
