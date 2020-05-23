#!/usr/bin/env python3

"""Unit tests for the string_processing.py module."""

from dvk_archive.processing.string_processing import extend_int
from dvk_archive.processing.string_processing import get_extension
from dvk_archive.processing.string_processing import get_filename
from dvk_archive.processing.string_processing import truncate_string


def test_extend_int():
    """Test the extend_int function."""
    assert extend_int() == "0"
    assert extend_int(None, 5) == "00000"
    assert extend_int(15, None) == "0"
    assert extend_int(256, 2) == "00"
    assert extend_int(12, 0) == "0"
    assert extend_int(15, 2) == "15"
    assert extend_int(input_int=12, input_length=5) == "00012"


def test_get_extension():
    """Test the get_extension function."""
    assert get_extension() == ""
    assert get_extension(None) == ""
    assert get_extension("") == ""
    assert get_extension("test") == ""
    assert get_extension("http://url.com/linksNstuff") == ""
    assert get_extension("/dot.folder/file.py") == ".py"
    assert get_extension("file.txt") == ".txt"
    assert get_extension("http://url.com/linksNstuff/file.png") == ".png"
    assert get_extension("http://url.kstuff/file.png?tokens'nstuff") == ".png"
    assert get_extension("http:/file?.jpeg?bleh") == ".jpeg"


def test_get_filename():
    """Test the get_filename function."""
    assert get_filename() == "0"
    assert get_filename(None) == "0"
    assert get_filename("") == "0"
    assert get_filename("This & That 2") == "This - That 2"
    assert get_filename("! !end filler!??  ") == "end filler"
    assert get_filename("$") == "0"
    assert get_filename("thing--stuff  @*-   bleh") == "thing-stuff - bleh"
    assert get_filename("a% - !b @  ??c") == "a - b - c"


def test_truncate_string():
    """Test the truncate_string function."""
    assert truncate_string() == ""
    assert truncate_string("blah") == ""
    assert truncate_string("bleh", -1) == ""
    assert truncate_string("words", 3) == "wor"
    assert truncate_string("word-stuff", 5) == "word"
    assert truncate_string("words n stuff", 4) == "stu"
    assert truncate_string("word stuff", 5) == "word"
    assert truncate_string("words-n-stuff", 4) == "stu"
    i = "This string is way too long to work as a title p25"
    o = "This string is way too long to work p25"
    assert truncate_string(i, 40) == o
    i = "HereIsA LongThingWithoutManySpacesWhichCanBeShort"
    o = "HereIsA WithoutManySpacesWhichCanBeShort"
    assert truncate_string(i, 40) == o
    i = "ThisMessageIsAbsolutelyWayToLongToWorkFor-"
    i = i + "AnyThingAtAllSoLetsSeeHowThisWillFareISuppose"
    o = "ThisMessageIsAbsolutelyWayToLongToWorkFo"
    assert truncate_string(i, 40) == o
    i = "ThisMessageIsAbsolutelyWayToLongToWorkForAnyThing-"
    i = i + "AtAllSoLetsSeeHowThisWillFareISuppose"
    o = "Th-AtAllSoLetsSeeHowThisWillFareISuppose"
    assert truncate_string(i, 40) == o
    i = "ThisLongTitleHasNoSpacesAtAllSoItHasAMiddleBreak"
    o = "ThisLongTitleHasAtAllSoItHasAMiddleBreak"
    assert truncate_string(i, 40) == o


def run_all():
    """Test all functions in the string_processing.py module."""
    test_extend_int()
    test_get_extension()
    test_get_filename()
    test_truncate_string()
