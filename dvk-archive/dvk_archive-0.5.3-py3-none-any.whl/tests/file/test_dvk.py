#!/usr/bin/env python3

"""Unit tests for the Dvk class."""

from json import dump
from shutil import rmtree
from os import listdir, mkdir, pardir, remove, stat
from os.path import abspath, exists, basename, join, expanduser
from dvk_archive.file.dvk import Dvk


def test_constructor():
    """Test the Dvk class constructor."""
    # CHECK EMPTY
    dvk = Dvk()
    assert dvk.get_title() is None
    assert dvk.get_id() == ""
    assert dvk.get_title() is None
    assert dvk.get_artists() == []
    assert dvk.get_time() == "0000/00/00|00:00"
    assert dvk.get_web_tags() is None
    assert dvk.get_description() is None
    assert dvk.get_page_url() is None
    assert dvk.get_direct_url() is None
    assert dvk.get_secondary_url() is None
    assert dvk.get_media_file() is None
    assert dvk.get_secondary_file() is None
    # GET FILENAME
    test_dir = abspath(join(expanduser("~"), "writeTest"))
    file_path = abspath(join(test_dir, "dvk1.dvk"))
    # SET DVK DATA
    dvk.set_id("id702")
    dvk.set_title("ConstructorTestTitle")
    dvk.set_artist("artistName")
    dvk.set_page_url("/url/")
    dvk.set_file(file_path)
    dvk.set_media_file("media.jpg")
    try:
        mkdir(test_dir)
        dvk.write_dvk()
        # CHECK VALUES
        loaded_dvk = Dvk(file_path)
        assert loaded_dvk.get_id() == "ID702"
        assert loaded_dvk.get_title() == "ConstructorTestTitle"
        assert loaded_dvk.get_artists()[0] == "artistName"
        assert loaded_dvk.get_page_url() == "/url/"
        assert basename(loaded_dvk.get_media_file()) == "media.jpg"
    finally:
        rmtree(test_dir)


def test_read_write_dvk():
    """Test the read_dvk and write_dvk functions."""
    # GET FILENAME
    test_dir = abspath(join(expanduser("~"), "readWrite"))
    dvk_path = abspath(join(test_dir, "dvk1.dvk"))
    # SET DVK DATA
    dvk = Dvk()
    dvk.set_file(dvk_path)
    dvk.set_id("id1234")
    dvk.set_title("WriteTestTitle")
    dvk.set_artists(["artist", "other artist"])
    dvk.set_time_int(1864, 10, 31, 7, 2)
    dvk.set_web_tags(["test", "Tags"])
    dvk.set_description("<b>desc</b>")
    dvk.set_page_url("http://somepage.com")
    dvk.set_direct_url("http://image.png")
    dvk.set_secondary_url("https://other.png")
    dvk.set_media_file("media.png")
    dvk.set_secondary_file("2nd.jpeg")
    # WRITE THEN READ
    try:
        mkdir(test_dir)
        dvk.write_dvk()
        dvk = Dvk()
        dvk.set_file(dvk_path)
        dvk.read_dvk()
        # CHECK VALUES
        assert dvk.get_id() == "ID1234"
        assert dvk.get_title() == "WriteTestTitle"
        assert dvk.get_artists()[0] == "artist"
        assert dvk.get_artists()[1] == "other artist"
        assert dvk.get_time() == "1864/10/31|07:02"
        assert dvk.get_web_tags()[0] == "test"
        assert dvk.get_web_tags()[1] == "Tags"
        assert dvk.get_description() == "<b>desc</b>"
        assert dvk.get_page_url() == "http://somepage.com"
        assert dvk.get_direct_url() == "http://image.png"
        assert dvk.get_secondary_url() == "https://other.png"
        assert basename(dvk.get_media_file()) == "media.png"
        assert basename(dvk.get_secondary_file()) == "2nd.jpeg"
        # CHECK READING NON-EXISTANT FILE
        dvk.set_file(None)
        dvk.read_dvk()
        assert dvk.get_title() is None
        # CHECK READING INVALID FILE
        data = {"test": "nope"}
        invalid_path = abspath(join(test_dir, "inv.dvk"))
        try:
            with open(invalid_path, "w") as out_file:
                dump(data, out_file)
        except IOError:
            assert False
        dvk.read_dvk()
        assert dvk.get_title() is None
        # CHECK WRITING INVALID FILE
        invalid_dvk = Dvk()
        invalid_path = "nonExistant.dvk"
        invalid_dvk.set_file(invalid_path)
        assert not exists(invalid_path)
    finally:
        rmtree(test_dir)


def test_write_media():
    """Test the write_media function."""
    test_dir = abspath(join(expanduser("~"), "renameTest"))
    try:
        mkdir(test_dir)
        # INVALID DVK
        dvk = Dvk()
        dvk.set_id("ID123")
        dvk.set_title("Title")
        dvk.set_artist("Artist")
        dvk.set_file(abspath(join(test_dir, "dvk1.dvk")))
        dvk.set_media_file("media.jpg")
        dvk.set_direct_url("kjlmlwonluyhj")
        dvk.write_media()
        assert listdir(test_dir) == []
        # INVALID DIRECT URL
        dvk.set_page_url("/whatever")
        dvk.write_media()
        assert listdir(test_dir) == []
        # VALID MEDIA
        url = "http://www.pythonscraping.com/img/gifts/img6.jpg"
        dvk.set_direct_url(url)
        dvk.write_media()
        assert dvk.get_time() == "0000/00/00|00:00"
        assert exists(dvk.get_file())
        assert exists(dvk.get_media_file())
        assert stat(dvk.get_media_file()).st_size == 39785
        remove(dvk.get_file())
        remove(dvk.get_media_file())
        # INVALID SECONDARY URL
        dvk.set_secondary_file("second.jpg")
        dvk.set_secondary_url("lksjamelkwelkmwm")
        dvk.write_media()
        assert listdir(test_dir) == []
        # VALID DIRECT AND SECONDARY URLS
        dvk.set_secondary_url(url)
        dvk.write_media(True)
        assert dvk.get_time() == "2014/08/04|00:49"
        assert exists(dvk.get_file())
        assert exists(dvk.get_media_file())
        assert exists(dvk.get_secondary_file())
        assert stat(dvk.get_media_file()).st_size == 39785
        filename = dvk.get_secondary_file()
        assert stat(filename).st_size == 39785
    finally:
        # DELETE TEST FILES
        rmtree(test_dir)


def test_add_to_dict():
    """Test the add_to_dict function."""
    start_dict = dict()
    dvk = Dvk()
    end_dict = dvk.add_to_dict()
    assert end_dict is None
    end_dict = dvk.add_to_dict(start_dict)
    assert start_dict == end_dict
    end_dict = dvk.add_to_dict(start_dict, "key")
    assert start_dict == end_dict
    end_dict = dvk.add_to_dict(start_dict, None, "temp")
    assert start_dict == end_dict
    start_dict = dvk.add_to_dict(start_dict, "key", "string")
    assert dvk.get_from_dict(start_dict, ["key"]) == "string"
    start_dict = dvk.add_to_dict(start_dict, "other", 5)
    assert dvk.get_from_dict(start_dict, ["other"]) == 5


def test_get_from_dict():
    """Test the get_from_dict function."""
    int_dict = dict()
    int_dict["thing"] = "blah"
    dictionary = dict()
    dictionary["key"] = "Yes"
    dictionary["internal"] = int_dict
    dvk = Dvk()
    assert dvk.get_from_dict() is None
    assert dvk.get_from_dict(dictionary, None, None) is None
    assert dvk.get_from_dict(None, ["key"], "fallback") == "fallback"
    assert dvk.get_from_dict(dictionary, ["key"]) == "Yes"
    keys = ["internal", "thing"]
    assert dvk.get_from_dict(dictionary, keys) == "blah"
    keys = ["internal", "no_key"]
    assert dvk.get_from_dict(dictionary, keys) is None


def test_can_write():
    """Test the can_write function."""
    dvk = Dvk()
    dvk.set_file("not_real.dvk")
    dvk.set_id("id")
    dvk.set_title("title")
    dvk.set_artist("artist")
    dvk.set_page_url("page_url")
    dvk.set_media_file("media.png")
    assert dvk.can_write()
    dvk.set_file()
    assert not dvk.can_write()
    dvk.set_file("file.dvk")
    dvk.set_id()
    assert not dvk.can_write()
    dvk.set_id("id")
    dvk.set_title()
    assert not dvk.can_write()
    dvk.set_title("title")
    dvk.set_artist()
    assert not dvk.can_write()
    dvk.set_artist("artist")
    dvk.set_page_url()
    assert not dvk.can_write()
    dvk.set_page_url("page_url")
    dvk.set_media_file()
    assert not dvk.can_write()


def test_get_filename():
    """Test the get_filename function."""
    dvk = Dvk()
    assert dvk.get_filename() == ""
    dvk.set_title("Title")
    assert dvk.get_filename() == ""
    dvk.set_id("ID123")
    dvk.set_title(None)
    assert dvk.get_filename() == ""
    dvk.set_title("Yay  more-files!")
    assert dvk.get_filename() == "Yay more-files_ID123"
    dvk.set_title("")
    assert dvk.get_filename() == "0_ID123"


def test_rename_files():
    """Test the rename_files function."""
    test_dir = abspath(join(expanduser("~"), "renameFilesTest"))
    try:
        mkdir(test_dir)
        dvk = Dvk()
        dvk.set_file(join(test_dir, "dvk1.dvk"))
        dvk.set_id("DVK1234")
        dvk.set_title("Yay DVK!")
        dvk.set_artist("Me")
        dvk.set_page_url("/test")
        dvk.set_media_file("file.txt")
        dvk.set_secondary_file("second.png")
        open(dvk.get_media_file(), "a").close()
        open(dvk.get_secondary_file(), "a").close()
        dvk.write_dvk()
        dvk.rename_files()
        assert basename(dvk.get_file()) == "Yay DVK_DVK1234.dvk"
        assert exists(dvk.get_file())
        assert basename(dvk.get_media_file()) == "Yay DVK_DVK1234.txt"
        assert exists(dvk.get_media_file())
        assert basename(dvk.get_secondary_file()) == "Yay DVK_DVK1234.png"
        assert exists(dvk.get_secondary_file())
        # CHECK SPECIFIC NAME
        dvk.rename_files("different")
        assert basename(dvk.get_file()) == "different.dvk"
        assert exists(dvk.get_file())
        assert basename(dvk.get_media_file()) == "different.txt"
        assert exists(dvk.get_media_file())
        assert basename(dvk.get_secondary_file()) == "different.png"
        assert exists(dvk.get_secondary_file())
        # CHECK NO SECONDARY
        dvk.set_title("No Sec")
        dvk.set_secondary_file("Bleh")
        dvk.write_dvk()
        dvk.rename_files()
        dvk.set_secondary_file(None)
        dvk.write_dvk()
        dvk.rename_files()
        assert basename(dvk.get_file()) == "No Sec_DVK1234.dvk"
        assert exists(dvk.get_file())
        assert basename(dvk.get_media_file()) == "No Sec_DVK1234.txt"
        assert exists(dvk.get_media_file())
        # CHECK NO MEDIA
        dvk.set_title("No Med")
        dvk.set_media_file("nonexistant.png")
        dvk.write_dvk()
        dvk.rename_files()
        dvk.set_media_file(None)
        dvk.rename_files()
        assert basename(dvk.get_file()) == "No Med_DVK1234.dvk"
        assert exists(dvk.get_file())
    finally:
        # DELETE TEST FILES
        rmtree(test_dir)


def test_get_set_file():
    """Test the get_file and set_file functions."""
    dvk = Dvk()
    dvk.set_file()
    assert dvk.get_file() is None
    dvk.set_file(None)
    assert dvk.get_file() is None
    dvk.set_file("")
    assert dvk.get_file() is None
    dvk.set_file("test_path.dvk")
    assert basename(dvk.get_file()) == "test_path.dvk"


def test_generate_id():
    """Test the generate_id function."""
    dvk = Dvk()
    dvk.generate_id("DVK")
    assert dvk.get_id() == ""
    dvk.set_title("Title1")
    dvk.generate_id()
    assert dvk.get_id() == ""
    dvk.set_artist("artist")
    dvk.set_page_url("/url")
    dvk.generate_id()
    assert dvk.get_id() == "4309082618"
    dvk.generate_id("VGK")
    assert dvk.get_id() == "VGK4309082618"
    dvk.generate_id("VGK", extra="bleh")
    assert dvk.get_id() == "VGK9821911274"
    dvk.set_title("Title2")
    dvk.generate_id("DVK")
    assert dvk.get_id() == "DVK9413915306"


def test_get_set_id():
    """Test the get_id and set_id functions."""
    dvk = Dvk()
    dvk.set_id()
    assert dvk.get_id() == ""
    dvk.set_id(None)
    assert dvk.get_id() == ""
    dvk.set_id("id123")
    assert dvk.get_id() == "ID123"


def test_get_set_title():
    """Test the get_title and set_title functions."""
    dvk = Dvk()
    dvk.set_title()
    assert dvk.get_title() is None
    dvk.set_title(None)
    assert dvk.get_title() is None
    dvk.set_title("")
    assert dvk.get_title() == ""
    dvk.set_title("TestTitle")
    assert dvk.get_title() == "TestTitle"


def test_get_set_artists():
    """Test the get_artists, set_artists, and set_artist functions."""
    dvk = Dvk()
    dvk.set_artist()
    assert dvk.get_artists() == []
    dvk.set_artist(None)
    assert dvk.get_artists() == []
    dvk.set_artist("my_artist")
    assert len(dvk.get_artists()) == 1
    assert dvk.get_artists()[0] == "my_artist"
    dvk.set_artists()
    assert dvk.get_artists() == []
    dvk.set_artists(None)
    assert dvk.get_artists() == []
    ats = []
    ats.append("artist10")
    ats.append("artist10")
    ats.append("")
    ats.append(None)
    ats.append("artist1")
    ats.append("test10.0.20-stuff")
    ats.append("test10.0.0-stuff")
    dvk.set_artists(ats)
    assert len(dvk.get_artists()) == 4
    assert dvk.get_artists()[0] == "artist1"
    assert dvk.get_artists()[1] == "artist10"
    assert dvk.get_artists()[2] == "test10.0.0-stuff"
    assert dvk.get_artists()[3] == "test10.0.20-stuff"


def test_set_time_int():
    """Test the set_time_int function."""
    dvk = Dvk()
    dvk.set_time_int()
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(None, None, None, None, None)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID YEAR
    dvk.set_time_int(0, 10, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID MONTH
    dvk.set_time_int(2017, 0, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 13, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID DAY
    dvk.set_time_int(2017, 10, 0, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 32, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID HOUR
    dvk.set_time_int(2017, 10, 10, -1, 0)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 10, 24, 0)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID MINUTE
    dvk.set_time_int(2017, 10, 10, 7, -1)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 10, 7, 60)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST VALID TIME
    dvk.set_time_int(2017, 10, 10, 7, 0)
    assert dvk.get_time() == "2017/10/10|07:00"


def test_get_set_time():
    """Test the get_time and set_time functions."""
    dvk = Dvk()
    dvk.set_time()
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time(None)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("2017/10/06")
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("yyyy/mm/dd/hh/tt")
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("2017!10!06!05!00")
    assert dvk.get_time() == "2017/10/06|05:00"


def test_get_set_web_tags():
    """Test the get_web_tags and set_web_tags functions."""
    dvk = Dvk()
    dvk.set_web_tags()
    assert dvk.get_web_tags() is None
    dvk.set_web_tags(None)
    assert dvk.get_web_tags() is None
    dvk.set_web_tags([])
    assert dvk.get_web_tags() is None
    dvk.set_web_tags(["tag1", "Tag2", "other tag", "tag1", None, ""])
    assert len(dvk.get_web_tags()) == 3
    assert dvk.get_web_tags()[0] == "tag1"
    assert dvk.get_web_tags()[1] == "Tag2"
    assert dvk.get_web_tags()[2] == "other tag"


def test_get_set_description():
    """Test the get_description and set_description functions."""
    dvk = Dvk()
    dvk.set_description()
    assert dvk.get_description() is None
    dvk.set_description(None)
    assert dvk.get_description() is None
    dvk.set_description("")
    assert dvk.get_description() is None
    dvk.set_description("<i>Baño</i>")
    assert dvk.get_description() == "<i>Ba&#241;o</i>"


def test_get_set_page_url():
    """Test the get_page_url and set_page_url functions."""
    dvk = Dvk()
    dvk.set_page_url()
    assert dvk.get_page_url() is None
    dvk.set_page_url(None)
    assert dvk.get_page_url() is None
    dvk.set_page_url("")
    assert dvk.get_page_url() is None
    dvk.set_page_url("/Page/url")
    assert dvk.get_page_url() == "/Page/url"


def test_get_set_direct_url():
    """Test the get_direct_url and set_direct_url functions."""
    dvk = Dvk()
    dvk.set_direct_url()
    assert dvk.get_direct_url() is None
    dvk.set_direct_url(None)
    assert dvk.get_direct_url() is None
    dvk.set_direct_url("")
    assert dvk.get_direct_url() is None
    dvk.set_direct_url("/direct/URL")
    assert dvk.get_direct_url() == "/direct/URL"


def test_get_set_secondary_url():
    """Test the get_secondary_url and set_secondary_url functions."""
    dvk = Dvk()
    dvk.set_secondary_url()
    assert dvk.get_secondary_url() is None
    dvk.set_secondary_url(None)
    assert dvk.get_secondary_url() is None
    dvk.set_secondary_url("")
    assert dvk.get_secondary_url() is None
    dvk.set_secondary_url("/Secondary/Url")
    assert dvk.get_secondary_url() == "/Secondary/Url"


def test_get_set_media_file():
    """Test the get_media_file and set_media_file functions."""
    dvk = Dvk()
    dvk.set_media_file("bleh.png")
    assert dvk.get_media_file() is None
    test_dir = abspath(join(expanduser("~"), "medfiles"))
    try:
        mkdir(test_dir)
        dvk.set_file(join(test_dir, "media.dvk"))
        dvk.set_media_file("media.png")
        assert basename(dvk.get_media_file()) == "media.png"
        value1 = abspath(join(dvk.get_file(), pardir))
        value2 = abspath(join(dvk.get_media_file(), pardir))
        assert value1 == value2
        dvk.set_media_file()
        assert dvk.get_media_file() is None
        dvk.set_media_file(None)
        assert dvk.get_media_file() is None
        dvk.set_media_file("")
        assert dvk.get_media_file() is None
    finally:
        rmtree(test_dir)


def test_get_set_secondary_file():
    """Test the get_secondary_file and set_secondary_file functions."""
    dvk = Dvk()
    dvk.set_secondary_file("other.png")
    assert dvk.get_media_file() is None
    test_dir = abspath(join(expanduser("~"), "secmedfiles"))
    try:
        mkdir(test_dir)
        dvk.set_file(join(test_dir, "mine.dvk"))
        dvk.set_secondary_file("second.png")
        assert basename(dvk.get_secondary_file()) == "second.png"
        value = abspath(join(dvk.get_secondary_file(), pardir))
        value2 = abspath(join(dvk.get_file(), pardir))
        assert value2 == value
        dvk.set_secondary_file()
        assert dvk.get_secondary_file() is None
        dvk.set_secondary_file("")
        assert dvk.get_secondary_file() is None
        dvk.set_secondary_file(None)
        assert dvk.get_secondary_file() is None
    finally:
        rmtree(test_dir)


def run_all():
    """Test all functions in the Dvk class."""
    test_constructor()
    test_read_write_dvk()
    test_write_media()
    test_add_to_dict()
    test_get_from_dict()
    test_can_write()
    test_get_filename()
    test_rename_files()
    test_get_set_file()
    test_generate_id()
    test_get_set_id()
    test_get_set_title()
    test_get_set_artists()
    test_set_time_int()
    test_get_set_time()
    test_get_set_web_tags()
    test_get_set_description()
    test_get_set_page_url()
    test_get_set_direct_url()
    test_get_set_secondary_url()
    test_get_set_media_file()
    test_get_set_secondary_file()
