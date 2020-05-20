from typing import Dict, List

from beets.ui import UserError


def _validate_tag_modification_argumens(arguments: List[str]) -> None:
    if len(arguments) == 0:
        raise UserError("Missing arguments for pattern and replacements!")

    if len(arguments) % 2 != 0:
        raise UserError(
            "Odd number of arguments. Any pattern is missing an replacement!"
        )


def _match_pattern_to_replacements(arguments: List[str]) -> Dict[str, str]:
    return {
        arguments[index]: arguments[index + 1]
        for index in range(0, len(arguments), 2)
    }


def parse_arguments_as_tag_modifications(
    arguments: List[str],
) -> Dict[str, str]:
    _validate_tag_modification_argumens(arguments)
    return _match_pattern_to_replacements(arguments)
