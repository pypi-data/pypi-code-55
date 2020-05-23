#!/usr/bin/env python3

"""Unit tests for the string_compare.py module."""

from dvk_archive.processing.string_compare import compare_alphanum
from dvk_archive.processing.string_compare import compare_sections
from dvk_archive.processing.string_compare import compare_strings
from dvk_archive.processing.string_compare import get_section
from dvk_archive.processing.string_compare import is_digit
from dvk_archive.processing.string_compare import is_number_string


def test_compare_strings():
    """Test the compare_strings function."""
    assert compare_strings() == 0
    assert compare_strings(None, "a") == 0
    assert compare_strings("b", None) == 0
    assert compare_strings(None, None) == 0
    assert compare_strings("B", "a") == 1
    assert compare_strings("a", "B") == -1
    assert compare_strings("Test1", "Test2") == -1
    assert compare_strings("Same", "same") == 0


def test_compare_alphanum():
    """Test the compare_alphanum function."""
    assert compare_alphanum() == 0
    assert compare_alphanum(None, "a") == 0
    assert compare_alphanum("b", None) == 0
    assert compare_alphanum(None, None) == 0
    assert compare_alphanum("B", "a") == 1
    assert compare_alphanum("a", "B") == -1
    assert compare_alphanum("Test1", "Test2") == -1
    assert compare_alphanum("string 100", "String 2") == 1
    assert compare_alphanum("Same25", "same25") == 0
    assert compare_alphanum("Test 0.5", "Test 0,05") == 1
    assert compare_alphanum("v1.2.10", "v1.2.02") == 1
    assert compare_alphanum("Thing 5 Extra", "Thing 20") == -1


def test_get_section():
    """Test the get_section function."""
    assert get_section() == ""
    assert get_section("") == ""
    assert get_section(None) == ""
    assert get_section("Some Text") == "Some Text"
    assert get_section("Test#1 - Other") == "Test#"
    assert get_section("256") == "256"
    assert get_section("15 Thing") == "15"
    assert get_section("10.5") == "10"
    assert get_section(".25 Text") == ".25"
    assert get_section(",50.2 Thing") == ",50"
    assert get_section("Test, and stuff.!") == "Test, and stuff.!"
    assert get_section("Number: .02!") == "Number: "
    assert get_section("# ,40") == "# "


def test_is_digit():
    """Test the is_digit function."""
    assert not is_digit()
    assert not is_digit("")
    assert not is_digit(None)
    assert not is_digit("long")
    assert is_digit("0")
    assert is_digit("9")
    assert is_digit("5")
    assert not is_digit("/")
    assert not is_digit(":")
    assert not is_digit("A")


def test_is_number_string():
    """Test the is_number_string function."""
    assert not is_number_string()
    assert not is_number_string("")
    assert not is_number_string(None)
    assert not is_number_string("string02")
    assert is_number_string("25 Thing")
    assert is_number_string(".34 String")
    assert is_number_string(",53.4")
    assert not is_number_string(".not number")
    assert not is_number_string(", nope")


def test_compare_sections():
    """Test the compare_sections function."""
    assert compare_sections() == 0
    assert compare_sections("", "a") == -1
    assert compare_sections("word", "") == 1
    assert compare_sections("text", "58") == 1
    assert compare_sections("24", "string") == -1
    assert compare_sections("2.5", "2.5") == 0
    assert compare_sections("10", "1") == 1
    assert compare_sections("10.05", "010.5") == -1
    assert compare_sections(".2", ".02") == 1
    assert compare_sections("10,05", "010,5") == -1
    assert compare_sections(",2", ",02") == 1
    assert compare_sections("0000000001", "0") == 1
    assert compare_sections("12.05.03", "2") == 0
    section1 = "12345678900000000000000000000000000000000000000000000"
    section2 = "12345678900000000000000000000000000000000000000000001"
    assert compare_sections(section1, section2) == -1
    section1 = "0.12345678900000000000000000000000000000000000000000000"
    section2 = "0.12345678900000000000000000000000000000000000000000001"
    assert compare_sections(section1, section2) == -1


def run_all():
    """Test all functions in the string_compare.py module."""
    test_compare_strings()
    test_compare_alphanum()
    test_get_section()
    test_is_digit()
    test_is_number_string()
    test_compare_sections()
