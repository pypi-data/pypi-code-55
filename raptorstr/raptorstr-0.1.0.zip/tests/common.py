# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg


from typing import Sequence, NamedTuple


class CaseEntry(NamedTuple):
    normal: str
    tokenized: Sequence[str]
    snake_case: str
    camel_case: str
    pascal_case: str
    kebab_case: str


TABLE_OF_CASES = (
    CaseEntry(
        normal="a",
        tokenized=["a"],
        snake_case="a",
        camel_case="a",
        pascal_case="A",
        kebab_case="a",
    ),
    CaseEntry(
        normal="aa",
        tokenized=["aa"],
        snake_case="aa",
        camel_case="aa",
        pascal_case="Aa",
        kebab_case="aa",
    ),
    CaseEntry(
        normal="a1",
        tokenized=["a1"],
        snake_case="a1",
        camel_case="a1",
        pascal_case="A1",
        kebab_case="a1",
    ),
    CaseEntry(
        normal="AA",
        tokenized=["aa"],
        snake_case="aa",
        camel_case="aa",
        pascal_case="Aa",
        kebab_case="aa",
    ),
    CaseEntry(
        normal="AAA",
        tokenized=["aaa"],
        snake_case="aaa",
        camel_case="aaa",
        pascal_case="Aaa",
        kebab_case="aaa",
    ),
    CaseEntry(
        normal="AAa",
        tokenized=["aaa"],
        snake_case="aaa",
        camel_case="aaa",
        pascal_case="Aaa",
        kebab_case="aaa",
    ),
    CaseEntry(
        normal="AAAa",
        tokenized=["aa", "aa"],
        snake_case="aa_aa",
        camel_case="aaAa",
        pascal_case="AaAa",
        kebab_case="aa-aa",
    ),
    CaseEntry(
        normal="one two",
        tokenized=["one", "two"],
        snake_case="one_two",
        camel_case="oneTwo",
        pascal_case="OneTwo",
        kebab_case="one-two",
    ),
    CaseEntry(
        normal="is ABR",  # is Abbreviation
        tokenized=["is", "abr"],
        snake_case="is_abr",
        camel_case="isAbr",
        pascal_case="IsAbr",
        kebab_case="is-abr",
    ),
    CaseEntry(
        normal="isABR",  # is Abbreviation
        tokenized=["is", "abr"],
        snake_case="is_abr",
        camel_case="isAbr",
        pascal_case="IsAbr",
        kebab_case="is-abr",
    ),
    CaseEntry(
        normal="ISAbr",  # is Abbreviation
        tokenized=["is", "abr"],
        snake_case="is_abr",
        camel_case="isAbr",
        pascal_case="IsAbr",
        kebab_case="is-abr",
    ),
    CaseEntry(
        normal="isABRAttr",  # is Abbreviation Attribute
        tokenized=["is", "abr", "attr"],
        snake_case="is_abr_attr",
        camel_case="isAbrAttr",
        pascal_case="IsAbrAttr",
        kebab_case="is-abr-attr",
    ),
)
