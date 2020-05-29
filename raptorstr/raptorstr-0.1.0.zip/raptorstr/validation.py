# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg


from raptorstr import snake_case, camel_case, pascal_case, kebab_case


def is_snake_case(string: str) -> bool:
    return snake_case(string) == string


def is_camel_case(string: str) -> bool:
    return camel_case(string) == string


def is_pascal_case(string: str) -> bool:
    return pascal_case(string) == string


def is_kebab_case(string: str) -> bool:
    return kebab_case(string) == string
