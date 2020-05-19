"""Tests for output printers."""

import re
from pytest import fixture, raises
from mc_nag.base_utils import read_template_file
from mc_nag.base_utils.models.rule import WARNING as RULE_WARNING
from mc_nag.base_utils.printers import OutputPrinter
from tests.rules.custom.custom_rule_for_option_testing import \
    CustomPlatformRule
from tests.fixtures import TestResource, TestTemplate

TEMPLATES_PATH = 'tests/templates'
VALID_TEMPLATE = f'{TEMPLATES_PATH}/parser_test_good.json'

# pylint: disable=redefined-outer-name


@fixture(scope="module")
def valid_template_evaluation():
    """Return violations after evaluating a valid template."""
    return ({}, {}, [CustomPlatformRule])


@fixture(scope="module")
def invalid_template_evaluation():
    """Return violations after evaluating an invalid template."""
    return (
        {CustomPlatformRule: [
            TestResource(
                resource_type='Microsoft.Storage/storageAccounts',
                resource_name='insecurestorageaccount',
                properties={'supportsHttpsTrafficOnly': True},
                raw_string="{'type': 'Microsoft.Storage/storageAccounts', " +
                "'apiVersion': '2019-04-01', 'name': " +
                "'insecurestorageaccount', 'location': 'eastus', 'sku':" +
                " {'name': 'Standard_LRS'}, 'kind': 'StorageV2', " +
                "'properties': {'supportsHttpsTrafficOnly': True}}",
                line_number=8
            )
        ]},
        {'WARNING': 1},
        [CustomPlatformRule]
    )


def test_template_output_good_template(capsys):
    """Happy Path: Ensure we can print a proper template."""
    template_model = TestTemplate(read_template_file(VALID_TEMPLATE))
    print(template_model)

    captured = capsys.readouterr()
    assert re.search('RESOURCES', captured.out)
    assert re.search('Resource Line Number: 45', captured.out)


def test_template_output_bad_template(capsys):
    """Sad Path: Ensure AttributeError is raised with bad template."""
    template_model = None
    print(template_model)

    captured = capsys.readouterr()
    assert re.match(r'^None$', captured.out)


def test_text_printer_no_violations(capsys, valid_template_evaluation):
    """Happy Path: Ensure proper output is printed with no violations."""
    violations_dict, violations_count, rules = valid_template_evaluation
    OutputPrinter.text(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert re.search('No violations', captured.out)


def test_text_printer_with_violations(capsys, invalid_template_evaluation):
    """Happy Path: Ensure proper output is printed with violations."""
    violations_dict, violations_count, rules = invalid_template_evaluation
    OutputPrinter.text(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert re.search('CustomPlatformRule', captured.out)
    assert re.search(fr'{RULE_WARNING}.* : 1', captured.out)


def test_text_printer_bad_violations_data():
    """Happy Path: Ensure proper output is printed with bad."""
    with raises(AttributeError, match="'str' object has no attribute"):
        OutputPrinter.text({'bad': 'data'}, {'bad': 'data'}, [])


def test_json_printer_no_violations(capsys, valid_template_evaluation):
    """Happy Path: Ensure proper output is printed with no violations."""
    violations_dict, violations_count, rules = valid_template_evaluation
    OutputPrinter.json(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert re.search(r'"violations": \[\]', captured.out)
    assert re.search(r'"report": {.*"total_violations": 0', captured.out)
    assert re.search(r'"report": {.*"rules_evaluated": \["CustomPlatformRule"\]',
                     captured.out)


def test_json_printer_with_violations(capsys, invalid_template_evaluation):
    """Happy Path: Ensure proper output is printed with violations."""
    violations_dict, violations_count, rules = invalid_template_evaluation
    OutputPrinter.json(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert re.search(r'"violations": \[{"name": "CustomPlatformRule',
                     captured.out)
    assert re.search(r'"report": {.*"total_violations": 1, "WARNING": 1',
                     captured.out)


def test_json_printer_bad_violations_data():
    """Happy Path: Ensure proper output is printed with bad data."""
    with raises(AttributeError, match="'str' object has no attribute"):
        OutputPrinter.json({'bad': 'data'}, {'bad': 'data'}, [])


def test_yaml_printer_no_violations(capsys, valid_template_evaluation):
    """Happy Path: Ensure proper output is printed with no violations."""
    violations_dict, violations_count, rules = valid_template_evaluation
    OutputPrinter.yaml(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert re.search(r'violations:', captured.out)
    assert re.search(r'^report:\n(.*\n)*\s+total_violations: 0',
                     captured.out, re.MULTILINE)
    assert re.search(r'^report:\n(.*\n)*\s+rules_evaluated:\n\s+- CustomPlatformRule',
                     captured.out, re.MULTILINE)


def test_yaml_printer_with_violations(capsys, invalid_template_evaluation):
    """Happy Path: Ensure proper output is printed with violations."""
    violations_dict, violations_count, rules = invalid_template_evaluation
    OutputPrinter.yaml(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert re.search(r"  name: CustomPlatformRule", captured.out)
    assert re.search(r"violations:\n- description: Testing the .*\n",
                     captured.out, re.MULTILINE)
    assert re.search(r'report:\n(.*\n)*\s+WARNING: 1',
                     captured.out, re.MULTILINE)
    assert re.search(r'report:\n(.*\n)*\s+total_violations: 1',
                     captured.out, re.MULTILINE)
    assert re.search(r'report:\n(.*\n)*\s+rules_evaluated:\n\s+- CustomPlatformRule',
                     captured.out, re.MULTILINE)


def test_yaml_printer_bad_violations_data():
    """Happy Path: Ensure proper output is printed with bad data."""
    with raises(AttributeError, match="'str' object has no attribute"):
        OutputPrinter.yaml({'bad': 'data'}, {'bad': 'data'}, [])


def test_none_printer_no_violations(capsys, valid_template_evaluation):
    """Happy Path: Ensure proper output is printed with no violations."""
    violations_dict, violations_count, rules = valid_template_evaluation
    OutputPrinter.none(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert not captured.out


def test_none_printer_with_violations(capsys, invalid_template_evaluation):
    """Happy Path: Ensure proper output is printed with violations."""
    violations_dict, violations_count, rules = invalid_template_evaluation
    OutputPrinter.none(violations_dict, violations_count, rules)

    captured = capsys.readouterr()
    assert not captured.out


def test_none_printer_bad_violations_data(capsys):
    """Happy Path: Ensure proper output is printed with bad data."""
    OutputPrinter.none({'bad': 'data'}, {'bad': 'data'}, [])

    captured = capsys.readouterr()
    assert not captured.out
