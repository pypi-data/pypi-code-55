#!/usr/bin/env python3

"""Unit tests for the DvkHandler class."""

from shutil import rmtree
from os import mkdir
from os.path import abspath, basename, expanduser, join
from dvk_archive.file.dvk import Dvk
from dvk_archive.file.dvk_handler import DvkHandler


class TestDvkHandler():
    """
    Unit tests for the DvkHandler class.

    Attributes:
        test_dir (str): Directory for holding test files.
    """

    def set_up(self):
        """Set up test files before running tests."""
        self.test_dir = abspath(join(expanduser("~"), "handlerTest"))
        mkdir(self.test_dir)
        dvk = Dvk()
        dvk.set_file(abspath(join(self.test_dir, "dvk.dvk")))
        dvk.set_id("Unimportant")
        dvk.set_page_url("/unimportant")
        dvk.set_direct_url("/thing")
        dvk.set_media_file("unimportant")
        count = 0
        while count < 2:
            dvk_file = join(self.test_dir, "dvk" + str(count) + ".dvk")
            dvk.set_file(dvk_file)
            dvk.set_title("DVK " + str(10 - count))
            dvk.set_artist("Thing")
            dvk.set_time_int(2019, 11, 8, 12, 20 - count)
            dvk.write_dvk()
            count = count + 1
        # SUB-DIRECTORY 1
        sub1 = abspath(join(self.test_dir, "sub1"))
        mkdir(sub1)
        while count < 4:
            dvk_file = join(sub1, "dvk" + str(10 - count) + ".dvk")
            dvk.set_file(dvk_file)
            dvk.set_title("DVK " + str(10 - count))
            dvk.set_artist("Artist" + str(10 - count))
            dvk.set_time_int(2019, 11, 8, 12, 10 - count)
            dvk.write_dvk()
            count = count + 1
        # SUB-DIRECTORY 2
        sub2 = abspath(join(self.test_dir, "sub2"))
        mkdir(sub2)
        while count < 6:
            dvk_file = join(sub2, "dvk" + str(10 - count) + ".dvk")
            dvk.set_file(dvk_file)
            dvk.set_title("DVK " + str(10 - count))
            dvk.set_artist("Thing")
            dvk.set_time_int(2019, 11, 8, 12, 30 - count)
            dvk.write_dvk()
            count = count + 1
        # INTERNAL SUB-DIRECTORY
        int_sub = abspath(join(sub2, "intSub"))
        mkdir(int_sub)
        while count < 8:
            dvk_file = join(int_sub, "dvk" + str(10 - count) + ".dvk")
            dvk.set_file(dvk_file)
            dvk.set_title("DVK " + str(10 - count))
            dvk.set_artist("Thing")
            dvk.set_time_int(2019, 11, 8, 12, 10 - count)
            dvk.write_dvk()
            count = count + 1
        empty_sub = abspath(join(sub2, "empty"))
        mkdir(empty_sub)

    def tear_down(self):
        """Remove all test files."""
        rmtree(self.test_dir)

    def test_reset_sorted(self):
        """Test the reset_sorted function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            assert dvk_handler.get_size() == 8
            count = 0
            while count < len(dvk_handler.sorted):
                assert dvk_handler.sorted[count] == count
                count = count + 1
            dvk_handler.load_dvks()
            assert dvk_handler.sorted == []
        finally:
            self.tear_down()

    def test_get_dvk_direct(self):
        """Test the get_dvk_direct function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            assert dvk_handler.get_dvk_direct().get_title() is None
            assert dvk_handler.get_dvk_direct(-1).get_title() is None
            assert dvk_handler.get_dvk_direct(8).get_title() is None
            print("NUMBER" + str(dvk_handler.get_size()))
            assert dvk_handler.get_size() == 8
            titles = []
            for i in range(0, 8):
                dvk = dvk_handler.get_dvk_direct(i)
                assert dvk.get_title() not in titles
                titles.append(dvk.get_title())
        finally:
            self.tear_down()

    def test_get_size(self):
        """Test the get_size function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            assert dvk_handler.get_size() == 8
            dvk_handler.load_dvks(None)
            assert dvk_handler.get_size() == 0
            dvk_file = abspath(join(self.test_dir, "sub1"))
            dvk_handler.load_dvks([dvk_file])
            assert dvk_handler.get_size() == 2
        finally:
            self.tear_down()

    def test_get_directories(self):
        """Test the get_directories function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            paths = dvk_handler.get_directories([self.test_dir])
            assert len(paths) == 4
            assert basename(paths[0]) == "handlerTest"
            assert basename(paths[1]) == "sub1"
            assert basename(paths[2]) == "sub2"
            assert basename(paths[3]) == "intSub"
            dvk_file = abspath(join(self.test_dir, "sub2"))
            paths = dvk_handler.get_directories([dvk_file])
            assert len(paths) == 2
            assert basename(paths[0]) == "sub2"
            assert basename(paths[1]) == "intSub"
            assert dvk_handler.get_directories() == []
            assert dvk_handler.get_directories(None) == []
            assert dvk_handler.get_directories("lskdfjo") == []
            s_paths = []
            s_paths.append(abspath(join(self.test_dir, "sub1")))
            s_paths.append(abspath(join(self.test_dir, "sub2")))
            paths = dvk_handler.get_directories(s_paths)
            assert len(paths) == 3
            assert basename(paths[0]) == "sub1"
            assert basename(paths[1]) == "sub2"
            assert basename(paths[2]) == "intSub"
            # EMPTY FOLDER
            empty_dir = join(self.test_dir, "empty")
            mkdir(empty_dir)
            paths = dvk_handler.get_directories([empty_dir])
            assert len(paths) == 1
            assert basename(paths[0]) == "empty"
        finally:
            self.tear_down()

    def test_contains_page_url(self):
        """Test the contains_page_url function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            assert not dvk_handler.contains_page_url()
            assert not dvk_handler.contains_page_url("bleh")
            dvk_handler.load_dvks([self.test_dir])
            assert not dvk_handler.contains_page_url()
            assert not dvk_handler.contains_page_url("bleh")
            assert dvk_handler.contains_page_url("/unimportant")
        finally:
            self.tear_down()

    def test_contains_direct_url(self):
        """Test the contains_page_url function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            assert not dvk_handler.contains_direct_url()
            assert not dvk_handler.contains_direct_url("bleh")
            dvk_handler.load_dvks([self.test_dir])
            assert not dvk_handler.contains_direct_url()
            assert not dvk_handler.contains_direct_url("bleh")
            assert dvk_handler.contains_direct_url("/thing")
        finally:
            self.tear_down()

    def test_contains_id(self):
        """Test the contains_id function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            assert not dvk_handler.contains_id()
            assert not dvk_handler.contains_id("bleh")
            dvk_handler.load_dvks([self.test_dir])
            assert not dvk_handler.contains_id()
            assert not dvk_handler.contains_id("bleh")
            assert dvk_handler.contains_id("UNIMPORTANT")
        finally:
            self.tear_down()

    def test_add_dvk(self):
        """Test the add_dvk function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            assert dvk_handler.get_size() == 8
            dvk_handler.add_dvk()
            assert dvk_handler.get_size() == 8
            dvk = Dvk()
            dvk.set_title()
            dvk_handler.add_dvk(dvk)
            assert dvk_handler.get_size() == 9
        finally:
            self.tear_down()

    def test_sort_dvks_alpha(self):
        """Test alpha-numeric sorting with the sort_dvks function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            dvk_handler.sort_dvks("a", False)
            assert dvk_handler.get_dvk_sorted(0).get_title() == "DVK 3"
            assert dvk_handler.get_dvk_sorted(1).get_title() == "DVK 4"
            assert dvk_handler.get_dvk_sorted(2).get_title() == "DVK 5"
            assert dvk_handler.get_dvk_sorted(3).get_title() == "DVK 6"
            assert dvk_handler.get_dvk_sorted(4).get_title() == "DVK 7"
            assert dvk_handler.get_dvk_sorted(5).get_title() == "DVK 8"
            assert dvk_handler.get_dvk_sorted(6).get_title() == "DVK 9"
            assert dvk_handler.get_dvk_sorted(7).get_title() == "DVK 10"
            # GROUP ARTISTS
            dvk_handler.sort_dvks("a", True)
            assert dvk_handler.get_dvk_sorted(0).get_title() == "DVK 7"
            assert dvk_handler.get_dvk_sorted(0).get_artists() == ["Artist7"]
            assert dvk_handler.get_dvk_sorted(1).get_title() == "DVK 8"
            assert dvk_handler.get_dvk_sorted(1).get_artists() == ["Artist8"]
            assert dvk_handler.get_dvk_sorted(2).get_title() == "DVK 3"
            assert dvk_handler.get_dvk_sorted(2).get_artists() == ["Thing"]
            assert dvk_handler.get_dvk_sorted(3).get_title() == "DVK 4"
            assert dvk_handler.get_dvk_sorted(4).get_title() == "DVK 5"
            assert dvk_handler.get_dvk_sorted(5).get_title() == "DVK 6"
            assert dvk_handler.get_dvk_sorted(6).get_title() == "DVK 9"
            assert dvk_handler.get_dvk_sorted(7).get_title() == "DVK 10"
            # EMPTY
            dvk_handler.load_dvks()
            dvk_handler.sort_dvks("a", False)
            assert dvk_handler.get_size() == 0
        finally:
            self.tear_down()

    def test_sort_dvks_time(self):
        """Test sorting by time with the sort_dvks function."""
        try:
            self.set_up()
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            dvk_handler.sort_dvks("t", False)
            time = "2019/11/08|12:03"
            assert dvk_handler.get_dvk_sorted(0).get_time() == time
            time = "2019/11/08|12:04"
            assert dvk_handler.get_dvk_sorted(1).get_time() == time
            time = "2019/11/08|12:07"
            assert dvk_handler.get_dvk_sorted(2).get_time() == time
            time = "2019/11/08|12:08"
            assert dvk_handler.get_dvk_sorted(3).get_time() == time
            time = "2019/11/08|12:19"
            assert dvk_handler.get_dvk_sorted(4).get_time() == time
            time = "2019/11/08|12:20"
            assert dvk_handler.get_dvk_sorted(5).get_time() == time
            time = "2019/11/08|12:25"
            assert dvk_handler.get_dvk_sorted(6).get_time() == time
            time = "2019/11/08|12:26"
            assert dvk_handler.get_dvk_sorted(7).get_time() == time
            # GROUP ARTISTS
            dvk_handler.sort_dvks("t", True)
            time = "2019/11/08|12:07"
            assert dvk_handler.get_dvk_sorted(0).get_time() == time
            assert dvk_handler.get_dvk_sorted(0).get_artists() == ["Artist7"]
            time = "2019/11/08|12:08"
            assert dvk_handler.get_dvk_sorted(1).get_time() == time
            assert dvk_handler.get_dvk_sorted(1).get_artists() == ["Artist8"]
            time = "2019/11/08|12:03"
            assert dvk_handler.get_dvk_sorted(2).get_time() == time
            assert dvk_handler.get_dvk_sorted(2).get_artists() == ["Thing"]
            time = "2019/11/08|12:04"
            assert dvk_handler.get_dvk_sorted(3).get_time() == time
            time = "2019/11/08|12:19"
            assert dvk_handler.get_dvk_sorted(4).get_time() == time
            time = "2019/11/08|12:20"
            assert dvk_handler.get_dvk_sorted(5).get_time() == time
            time = "2019/11/08|12:25"
            assert dvk_handler.get_dvk_sorted(6).get_time() == time
            time = "2019/11/08|12:26"
            assert dvk_handler.get_dvk_sorted(7).get_time() == time
            # EMPTY
            dvk_handler.load_dvks()
            dvk_handler.sort_dvks("t", False)
            assert dvk_handler.get_size() == 0
        finally:
            self.tear_down()

    def run_all(self):
        """Test all functions in DvkHandler class."""
        self.test_get_directories()
        self.test_get_size()
        self.test_reset_sorted()
        self.test_get_dvk_direct()
        self.test_contains_id()
        self.test_contains_page_url()
        self.test_contains_direct_url()
        self.test_add_dvk()
        self.test_sort_dvks_alpha()
        self.test_sort_dvks_time()
