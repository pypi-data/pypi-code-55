import pytest

from zlibtui.menu import *

item1 = Item("item1",["1","2"],"A")
item2 = Item("item2",["3","4"],"B")

testMenu = Menu([item1,item2])

def test_getAll():

    assert testMenu.getAll() == {"A":"1","B":"3"}

def test_changeOption():
    testMenu.changeOption("right")
    assert testMenu.items[testMenu.itemSelected].optionSelected == 1 

    testMenu.changeOption("right")
    assert testMenu.items[testMenu.itemSelected].optionSelected == 0
    
    testMenu.changeOption("left")
    assert testMenu.items[testMenu.itemSelected].optionSelected == 1

    testMenu.changeOption("left")
    assert testMenu.items[testMenu.itemSelected].optionSelected == 0

