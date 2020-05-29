# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg


import pytest

from raptorstr import (
    is_snake_case,
    is_camel_case,
    is_pascal_case,
    is_kebab_case,
)
from tests.common import TABLE_OF_CASES


@pytest.mark.parametrize(
    "input, snake_case_string",
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
def test_is_snake_case(input, snake_case_string):
    if input == snake_case_string:
        assert is_snake_case(input)
    else:
        assert not is_snake_case(input)


@pytest.mark.parametrize(
    "input, camel_case_string",
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
def test_is_camel_case(input, camel_case_string):
    if input == camel_case_string:
        assert is_camel_case(input)
    else:
        assert not is_camel_case(input)


@pytest.mark.parametrize(
    "input, pascal_case_string",
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
def test_is_pascal_case(input, pascal_case_string):
    if input == pascal_case_string:
        assert is_pascal_case(input)
    else:
        assert not is_pascal_case(input)


@pytest.mark.parametrize(
    "input, kebab_case_string",
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
def test_is_kebab_case(input, kebab_case_string):
    if input == kebab_case_string:
        assert is_kebab_case(input)
    else:
        assert not is_kebab_case(input)
