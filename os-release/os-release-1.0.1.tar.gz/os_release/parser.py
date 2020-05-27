import re
from pathlib import Path

from arpeggio import ParserPython, PTNodeVisitor, visit_parse_tree, NoMatch

from os_release.grammar import os_release

PARSER = ParserPython(os_release, ws='\t ')


class OsReleaseParseException(BaseException):
    """Raised when the given ``os-release`` file or string cannot be parsed."""
    pass


class OsReleaseVisitor(PTNodeVisitor):
    def visit_os_release(self, node, children):
        return dict(children.variable)

    def visit_variable(self, node, children):
        return (children[0], children[1])

    def visit_quoted_string(self, node, children):
        escapes = [
            (r'\$', '$'),
            (r'\"', '"'),
            (r"\'", "'"),
            (r'\\', '\\'),
            (r'\`', '`'),
        ]

        value: str = children[0]
        for (old, new) in escapes:
            value = value.replace(old, new)

        return value


def parse_file(path: Path):
    try:
        root = PARSER.parse_file(path)

    except NoMatch:
        raise OsReleaseParseException(f"Failed to parse os-release file '{path}'.") from None

    return visit_parse_tree(root, OsReleaseVisitor())


def parse_str(s: str):
    try:
        root = PARSER.parse(s)

    except NoMatch:
        first_line = next(re.finditer(r'.*$', s))[0]
        raise OsReleaseParseException(f"Failed to parse os-release string '{first_line}'.") from None

    return visit_parse_tree(root, OsReleaseVisitor())