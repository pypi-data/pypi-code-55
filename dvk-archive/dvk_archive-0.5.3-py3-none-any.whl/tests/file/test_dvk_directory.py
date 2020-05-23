#!/usr/bin/env python3

"""Unit tests for the DvkDirectory class."""

from shutil import rmtree
from os import mkdir
from os.path import abspath, join, expanduser
from dvk_archive.file.dvk import Dvk
from dvk_archive.file.dvk_directory import DvkDirectory


class TestDvkDirectory():
    """
    Unit tests for the DvkDirectory class.

    Attributes:
        test_dir (str): Directory for holding DVK files used in testing.
        dvk_directory (DvkDirectory):
    """

    def set_up(self):
        """Initialize DvkDirectoryTest attributes for testing."""
        self.test_dir = abspath(join(expanduser("~"), "dirTest"))
        mkdir(self.test_dir)
        # DVK 1
        dvk = Dvk()
        dvk.set_file(join(self.test_dir, "dvk2.dvk"))
        dvk.set_id("Unimportant")
        dvk.set_title("DVK 2")
        dvk.set_artists(["Guy", "Other Guy"])
        dvk.set_time_int(2019, 11, 2, 12, 0)
        dvk.set_page_url("/unimportant")
        dvk.set_media_file("unimportant")
        dvk.write_dvk()
        # DVK 2
        dvk.set_time_int(2018, 11, 2, 11, 15)
        dvk.set_file(join(self.test_dir, "dvk2-2.dvk"))
        dvk.write_dvk()
        # DVK 3
        dvk.set_title("DVK 10")
        dvk.set_artist("Guy")
        dvk.set_time_int(2019, 11, 2, 11, 15)
        dvk.set_file(join(self.test_dir, "dvk10.dvk"))
        dvk.write_dvk()
        # DVK 4
        dvk.set_title("DVK 5.25 - Fun!")
        dvk.set_artist("Artist")
        dvk.set_time_int(2019, 5, 2, 5, 25)
        dvk.set_file(join(self.test_dir, "dvk5-25.dvk"))
        dvk.write_dvk()
        # DVK 5
        dvk.set_title("DVK 5 - Fun!")
        dvk.set_file(join(self.test_dir, "dvk5.dvk"))
        dvk.write_dvk()
        self.dvk_directory = DvkDirectory()
        self.dvk_directory.read_dvks(self.test_dir)

    def tear_down(self):
        """Delete test files after DvkDirectory testing."""
        rmtree(self.test_dir)

    def test_get_size(self):
        """Test the get_size function."""
        try:
            self.set_up()
            assert self.dvk_directory.get_size() == 5
            self.dvk_directory.read_dvks()
            assert self.dvk_directory.get_size() == 0
        finally:
            self.tear_down()

    def run_all(self):
        """Test all functions of the DvkDirectory class."""
        self.test_get_size()
