"""Tests for BaseParser."""

from pytest import raises
from mc_nag.base_utils.parser import BaseParser
from mc_nag.base_utils.exceptions import InvalidTemplate
from mc_nag.base_utils import read_template_file

TEMPLATES_PATH = 'tests/templates'


def test_base_parser_good_json():
    """Happy Path: Ensure parser can handle a basic template."""
    filepath = f'{TEMPLATES_PATH}/parser_test_good.json'

    with open(filepath) as template:
        template_string = template.read()

    parser = BaseParser(template_string)

    assert len(parser.resources) == 1
    assert parser.resources[0]['name'] == 'OnlyResource'
    with raises(InvalidTemplate):
        parser.validate_file('template', parser.parsed_template,
                            ['MISSING_KEY'])


def test_base_parser_bad_json():
    """Sad Path: Ensure parser throws exception for bad template."""
    filepath = f'{TEMPLATES_PATH}/parser_test_bad.json'

    with open(filepath) as template:
        template_string = template.read()

    with raises(InvalidTemplate, match=r"Invalid YAML or JSON syntax"):
        _ = BaseParser(template_string)


def test_base_parser_bad_line_number():
    """Sad Path: Ensure parser returns -1 when no line number found."""
    filepath = f'{TEMPLATES_PATH}/parser_test_good.json'

    with open(filepath) as template:
        template_string = template.read()

    parser = BaseParser(template_string)

    assert len(parser.resources) == 1
    assert parser.resources[0]['name'] == 'OnlyResource'
    assert parser.find_line_number('DOESNOTEXIST') == -1
    assert not parser.parameters
    assert not parser.outputs
    assert not parser.functions
    assert not parser.variables


def test_parser_bad_syntax_param_file():
    """Sad Path: Ensure parser throws exception for a bad Azure parameter JSON file.."""
    template_string = read_template_file(f'{TEMPLATES_PATH}/' +
                                         'parser_test_good.json')
    parameters_string = read_template_file(f'{TEMPLATES_PATH}/' +
                                           'parser_test_param_file_bad.json')

    with raises(InvalidTemplate, match=r"Invalid YAML or JSON syntax!"):
        _ = BaseParser(template_string, parameters_string)
