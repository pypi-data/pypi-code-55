#!/usr/bin/env python3

"""Unit tests for the list_processing.py module."""

from dvk_archive.processing.list_processing import clean_list
from dvk_archive.processing.list_processing import list_to_string
from dvk_archive.processing.list_processing import sort_alphanum


def test_clean_list():
    """Test the clean_list function."""
    assert len(clean_list()) == 0
    assert len(clean_list(None)) == 0
    cleaned = clean_list(["these", "are", "things", "", None, "are"])
    assert len(cleaned) == 3
    assert cleaned[0] == "these"
    assert cleaned[1] == "are"
    assert cleaned[2] == "things"


def test_list_to_string():
    """Test the list_to_string function."""
    assert list_to_string() == ""
    assert list_to_string(None) == ""
    assert list_to_string([""]) == ""
    assert list_to_string([None]) == ""
    assert list_to_string(["test"]) == "test"
    input = ["", "String1", None, None, "string 2", "3"]
    assert list_to_string(input) == "String1,string 2,3"


def test_sort_alphanum():
    """Test the sort_alphanum function."""
    list = ["10,05", "010,5", "5"]
    list = sort_alphanum(list)
    assert list == ["5", "10,05", "010,5"]
    assert sort_alphanum() == []
    assert sort_alphanum([]) == []


def run_all():
    """Test all functions of the list_processing.py module."""
    test_clean_list()
    test_list_to_string()
    test_list_to_string()
    test_sort_alphanum()
