#!/usr/bin/env python3

"""Unit tests for the basic_conect.py module."""

from shutil import rmtree
from os import listdir, stat, mkdir
from os.path import abspath, exists, expanduser, join
from dvk_archive.web.basic_connect import bs_connect
from dvk_archive.web.basic_connect import json_connect
from dvk_archive.web.basic_connect import basic_connect
from dvk_archive.web.basic_connect import download
from dvk_archive.web.basic_connect import get_last_modified
from dvk_archive.web.basic_connect import remove_header_footer


def test_bs_connect():
    """Test the bs_connect function."""
    assert bs_connect() is None
    assert bs_connect(None) is None
    assert bs_connect("") is None
    assert bs_connect("jkslkeerkn") is None
    assert bs_connect("http://lakjwj;wklk;okjovz") is None
    url = "http://pythonscraping.com/exercises/exercise1.html"
    bs = bs_connect(url)
    assert bs is not None
    assert bs.find("h1").get_text() == "An Interesting Title"


def test_basic_connect():
    """Test the basic_connect function."""
    assert basic_connect() is None
    assert basic_connect(None) is None
    assert basic_connect("") is None
    assert basic_connect("jkslkeerkn") is None
    assert basic_connect("http://lakjwj;wklk;okjovz") is None
    url = "http://pythonscraping.com/exercises/exercise1.html"
    html = basic_connect(url)
    assert html is not None
    assert html.startswith("<html>\n<head>\n<title>A Useful Page</title>")


def test_download():
    """Test the download function."""
    try:
        test_dir = abspath(join(expanduser("~"), "imageTests"))
        mkdir(test_dir)
        file = join(test_dir, "image.jpg")
        download()
        assert listdir(test_dir) == []
        download(url="http://www.pythonscraping.com/img/gifts/img6.jpg")
        assert listdir(test_dir) == []
        download(filename=file)
        assert listdir(test_dir) == []
        download(
            url="asfdwersdbsdfsd",
            filename=file)
        assert listdir(test_dir) == []
        url = "http://www.pythonscraping.com/img/gifts/img6.jpg"
        headers = download(url, file)
        assert exists(file)
        modified = ""
        try:
            modified = headers["Last-Modified"]
        except KeyError:
            pass
        assert modified == "Mon, 04 Aug 2014 00:49:03 GMT"
        assert stat(file).st_size == 39785
        download(
            url="http://www.pythonscraping.com/img/gifts/img6.jpg",
            filename=file)
        file = join(test_dir, "image(1).jpg")
        assert exists(file)
        assert stat(file).st_size == 39785
    finally:
        rmtree(test_dir)


def test_get_last_modified():
    """Test the get_last_modified function."""
    assert get_last_modified() == ""
    assert get_last_modified(dict()) == ""
    # TEST INVALID
    dic = {"Last-Modified": ""}
    assert get_last_modified(dic) == ""
    dic = {"Last-Modified": "Mon, BB Aug FFFF GG:TT:PP GMT"}
    assert get_last_modified(dic) == ""
    # TEST ALL MONTHS
    dic = {"Last-Modified": "Udf, 10 Jan 2010 12:05:55 GMT"}
    assert get_last_modified(dic) == "2010/01/10|12:05"
    dic = {"Last-Modified": "Udf, 23 Feb 2015 20:23:55 GMT"}
    assert get_last_modified(dic) == "2015/02/23|20:23"
    dic = {"Last-Modified": "Udf, 01 Mar 2019 12:00:55 GMT"}
    assert get_last_modified(dic) == "2019/03/01|12:00"
    dic = {"Last-Modified": "Udf, 10 Apr 2010 12:05:55 GMT"}
    assert get_last_modified(dic) == "2010/04/10|12:05"
    dic = {"Last-Modified": "Udf, 23 May 2015 20:23:55 GMT"}
    assert get_last_modified(dic) == "2015/05/23|20:23"
    dic = {"Last-Modified": "Udf, 01 Jun 2019 12:00:55 GMT"}
    assert get_last_modified(dic) == "2019/06/01|12:00"
    dic = {"Last-Modified": "Udf, 10 Jul 2010 12:05:55 GMT"}
    assert get_last_modified(dic) == "2010/07/10|12:05"
    dic = {"Last-Modified": "Udf, 23 Aug 2015 20:23:55 GMT"}
    assert get_last_modified(dic) == "2015/08/23|20:23"
    dic = {"Last-Modified": "Udf, 01 Sep 2019 12:00:55 GMT"}
    assert get_last_modified(dic) == "2019/09/01|12:00"
    dic = {"Last-Modified": "Udf, 10 Oct 2010 12:05:55 GMT"}
    assert get_last_modified(dic) == "2010/10/10|12:05"
    dic = {"Last-Modified": "Udf, 23 Nov 2015 20:23:55 GMT"}
    assert get_last_modified(dic) == "2015/11/23|20:23"
    dic = {"Last-Modified": "Udf, 01 Dec 2019 12:00:55 GMT"}
    assert get_last_modified(dic) == "2019/12/01|12:00"
    dic = {"Last-Modified": "Udf, 10 Nop 2010 12:05:55 GMT"}
    assert get_last_modified(dic) == ""


def test_remove_header_footer():
    """Test the remove_header_footer function."""
    assert remove_header_footer() == ""
    assert remove_header_footer("") == ""
    assert remove_header_footer("   ") == ""
    assert remove_header_footer("<p>") == ""
    assert remove_header_footer("<head><foot>") == ""
    assert remove_header_footer("<p>  test") == "test"
    assert remove_header_footer("test </p>") == "test"
    assert remove_header_footer("<head> Things   </foot>") == "Things"
    assert remove_header_footer("<div><p>bleh</p></div>") == "<p>bleh</p>"


def run_all():
    """Test all functions of the basic_connect.py module."""
    test_bs_connect()
    test_basic_connect()
    test_download()
    test_get_last_modified()
    test_remove_header_footer()
