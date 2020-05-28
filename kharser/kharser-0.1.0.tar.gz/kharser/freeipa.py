from typing import List, Dict
import re


def parse_users(extract: str) -> List[Dict]:
    parts = extract.split('\n\n')
    # filter comment
    return [parse_section(part) for part in parts]


def parse_records(record: str) -> dict:
    key, value = record.split(':')
    return {key.strip(): value.strip()}


def parse_section(section: str) -> dict:
    result = {}
    for elt in section.strip().split('\n'):
        result.update(parse_records(elt))
    return result
