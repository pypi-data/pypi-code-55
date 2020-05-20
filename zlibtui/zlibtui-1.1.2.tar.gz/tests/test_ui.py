import pytest

from zlibtui.ui import *

testBox = Box()

def test_write():

    testBox.write("This is a sentence")
    assert testBox.cursor_y == 3
    assert testBox.cursor_x == 1

    testBox.write("\n")
    assert testBox.cursor_y == 4

    testBox.write("\n"*100)
    assert testBox.cursor_y == 4

def test_clear():

    testBox.clear()
    testBox.write("this")
    testBox.clear()

    assert testBox.cursor_x == testBox.x + 1
    assert testBox.cursor_y == testBox.y + 1


testSearchBox = SearchBox()

def test_writeSearchBox():

    testSearchBox.write("This is a search")
    testSearchBox.write("a")
    assert testSearchBox.content == "This is a searcha"

def test_backspace():

    testSearchBox.backspace()
    assert testSearchBox.content == "This is a search"

def test_clearSearchBox():

    testSearchBox.clearContent()
    assert testSearchBox.content == ""




