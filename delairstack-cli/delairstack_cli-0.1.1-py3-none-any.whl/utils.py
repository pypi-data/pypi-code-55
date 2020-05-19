import itertools
import pprint
from typing import Dict, Union, List

import click_spinner
import jsonschema
import typer

# Replace default spinner with a prettier
SPINNER = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
click_spinner.Spinner.spinner_cycle = itertools.cycle(SPINNER)


def spinner():
    return click_spinner.spinner()


def validate_against_schema(instance: Union[Dict, List], *, json_schema: Dict):
    """Validate the given instance (object representation of a JSON string).

        Args:
            instance: The instance to validate.

            json_schema: JSON schema dict.

        """
    v = jsonschema.Draft7Validator(json_schema)
    errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
    if errors:
        reason = __create_validation_error_msg(errors)
        return reason
    else:
        return None


def __create_validation_error_msg(errors):
    error_msgs = []
    for error in errors:
        path = [str(sub_path) for sub_path in error.path]
        str_path = ''
        if path:
            str_path = '#/{}: '.format('/'.join(path))
        error_msg = ' - {}{}'.format(str_path, error.message)
        error_msgs.append(error_msg)
    return '\n'.join(error_msgs)


def check_json_schema(json_schema):
    if not json_schema:
        return

    try:
        jsonschema.Draft7Validator(json_schema).check_schema(json_schema)
    except jsonschema.SchemaError as e:
        typer.secho(
            '✖ Invalid JSON schema:\n{}'.format(
                pprint.pformat(json_schema, indent=2)),
            fg=typer.colors.RED
        )
        typer.secho('\ndetails: {}'.format(e.message), fg=typer.colors.RED)
        raise typer.Exit(2)
