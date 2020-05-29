# SPDX-License-Identifer: MPL-2.0
# Copyright © 2020 Andreas Stenberg


import re
import unicodedata
from typing import Generator

TOKENS = [
    ("CAP_TOK", r"[A-Z]+(?![a-z])"),
    ("STD_TOK", r"[A-Z]?[a-z]*[0-9]*"),
    ("SEPARATOR", r"[-_ ]"),
]


def tokenize_string(string: str) -> Generator[str, None, None]:
    sanitized_string = unicodedata.normalize("NFKC", string)
    token_regex = "|".join(f"(?P<{ident}>{regexp})" for ident, regexp in TOKENS)
    remainder = ""
    for mo in re.finditer(token_regex, sanitized_string):
        matched_text = mo.group()
        if matched_text and mo.lastgroup != "SEPARATOR":
            if len(matched_text) > 1:
                if remainder:
                    yield remainder + matched_text
                    remainder = ""
                else:
                    yield matched_text
            else:
                remainder += matched_text
    if remainder:
        yield remainder


def snake_case(string: str) -> str:
    return "_".join(p.lower() for p in tokenize_string(string))


def camel_case(string: str) -> str:
    parts = list(tokenize_string(string))
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def pascal_case(string: str) -> str:
    return "".join(p.capitalize() for p in tokenize_string(string))


def kebab_case(string: str) -> str:
    return "-".join(p.lower() for p in tokenize_string(string))
