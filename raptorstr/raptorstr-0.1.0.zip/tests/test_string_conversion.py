# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg


import pytest

from raptorstr import (
    snake_case,
    camel_case,
    pascal_case,
    kebab_case,
)
from raptorstr.formatting import tokenize_string
from tests.common import TABLE_OF_CASES


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (case, ce.tokenized)
        for ce in TABLE_OF_CASES
        for case in (
            ce.normal,
            ce.snake_case,
            ce.camel_case,
            ce.pascal_case,
            ce.kebab_case,
        )
    ],
)
def test_tokenizer(input, expected_output):
    assert [p.lower() for p in tokenize_string(input)] == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (case, ce.snake_case)
        for ce in TABLE_OF_CASES
        for case in (
            ce.normal,
            ce.snake_case,
            ce.camel_case,
            ce.pascal_case,
            ce.kebab_case,
        )
    ],
)
def test_snake_case(input, expected_output):
    assert snake_case(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (case, ce.camel_case)
        for ce in TABLE_OF_CASES
        for case in (
            ce.normal,
            ce.snake_case,
            ce.camel_case,
            ce.pascal_case,
            ce.kebab_case,
        )
    ],
)
def test_camel_case(input, expected_output):
    assert camel_case(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (case, ce.pascal_case)
        for ce in TABLE_OF_CASES
        for case in (
            ce.normal,
            ce.snake_case,
            ce.camel_case,
            ce.pascal_case,
            ce.kebab_case,
        )
    ],
)
def test_pascal_case(input, expected_output):
    assert pascal_case(input) == expected_output


@pytest.mark.parametrize(
    "input, expected_output",
    [
        (case, ce.kebab_case)
        for ce in TABLE_OF_CASES
        for case in (
            ce.normal,
            ce.snake_case,
            ce.camel_case,
            ce.pascal_case,
            ce.kebab_case,
        )
    ],
)
def test_kebab_case(input, expected_output):
    assert kebab_case(input) == expected_output
