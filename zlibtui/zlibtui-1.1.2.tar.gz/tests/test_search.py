import requests
import pytest

from zlibtui.search import *

testSearch = Search()

def test_nextPage():

    testSearch.nextPage()
    assert testSearch.searchOptions["page"] == "2"

def test_previousPage():

    testSearch.previousPage()
    assert testSearch.searchOptions["page"] == "1"

    testSearch.previousPage()
    assert testSearch.searchOptions["page"] == "1"

def test_updateSearchOptions():

    testSearch.updateSearchOptions()
    assert "matchPhrase" not in testSearch.searchOptions
    assert "language" in testSearch.searchOptions
    assert "extension" in testSearch.searchOptions
    
def test_executeSearch():

    assert testSearch.executeSearch().status_code == 200

def test_getResults():

    testSearch.input = "Camus"
    books = testSearch.getResults()
    assert len(books) == 50

def test_getDetails():
    pass


