from flake8parser import parse_line
from flake8parser import ParserError
from flake8parser import Violation
import pytest


@pytest.mark.parametrize(
    "line, violation",
    [
        (
            "./parse.py:2:5: F841 local variable 'thing' is assigned to but never used",
            Violation(
                path="./parse.py",
                line=2,
                column=5,
                letter="F",
                number=841,
                message="local variable 'thing' is assigned to but never used",
            ),
        ),
        (
            "./setup.py:5:1: F401 'os' imported but unused",
            Violation(
                path="./setup.py",
                line=5,
                column=1,
                letter="F",
                number=401,
                message="'os' imported but unused",
            ),
        ),
        (
            "./voluptuous/validators.py:106:6: N802 function name 'IsTrue' should be "
            "lowercase",
            Violation(
                path="./voluptuous/validators.py",
                line=106,
                column=6,
                letter="N",
                number=802,
                message="function name 'IsTrue' should be lowercase",
            ),
        ),
    ],
)
def test_parse_line(line: str, violation: Violation):
    assert parse_line(line) == violation
    assert str(violation) == line


@pytest.mark.parametrize("line", ["", "asdf"])
def test_parse_line_error(line: str):
    with pytest.raises(ParserError):
        parse_line(line)
