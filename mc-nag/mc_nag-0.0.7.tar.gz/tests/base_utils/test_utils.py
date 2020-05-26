"""Tests for utility functions."""

import os
import re
from mc_nag.base_utils import (
    find_key_in_structure,
    read_template_file
)


def test_find_key_in_structure():
    """Test finding keys in deep structures."""
    example_dict = {'key1': {'key2': 'val2', 'key3': {'key4': 'val4'}}}
    example_list = [
        'item1',
        ['item2', 'item3'],
        {'key1': {'key2': 'val2', 'key3': {'key4': 'val4'}}}
    ]

    assert 'val4' in find_key_in_structure('key4', example_dict)
    assert 'val4' in find_key_in_structure('key4', example_list)

    assert list(find_key_in_structure('key5', example_dict)) == []
    assert list(find_key_in_structure('key5', example_list)) == []


def test_read_template_file():
    """Test utility to open and read files."""
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/../../mc_nag/__init__.py'
    text_match = "__version__ = '"

    assert re.search(text_match, read_template_file(file_path))
