from typing import List, Dict, Pattern
from collections import defaultdict
import re


def _nocomment(text: str) -> str:
    pattern = r'-{5,}\n'
    matched = re.split(pattern, text, flags=re.M)
    return matched[2] if len(matched) > 2 else text


def _make_pattern(sep) -> str:
    return f'(?P<key>[^{sep} ]+){sep}(?P<value>.*)'


def parse_users(extract: str) -> List[Dict]:
    cleaned = _nocomment(extract)
    parts = cleaned.split('\n\n')
    # filter comment
    return [parse_section(part) for part in parts]


def _to_flat(data: defaultdict) -> dict:
    def unlist(elt):
        if len(elt) > 1:
            return elt
        elif elt:
            return elt[0]
        else:
            None
    return {unlist(k): unlist(v) for k, v in data.items()}


def parse_section(section: str) -> dict:
    result = defaultdict(list)
    pattern = re.compile(_make_pattern(':'))
    for elt in section.strip().split('\n'):
        matched = pattern.search(elt)
        if matched:
            result[matched.group('key').strip()].append(
                matched.group('value').strip())
    return _to_flat(result)
