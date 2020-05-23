#!/usr/bin/env python3

"""Unit tests for the rename_files.py module."""

from os import mkdir
from os.path import abspath, basename, exists, expanduser, join
from shutil import rmtree
from dvk_archive.file.dvk import Dvk
from dvk_archive.file.dvk_handler import DvkHandler
from dvk_archive.reformat.rename_files import rename_files


class TestRenameFiles():
    """
    Unit tests for the rename_files.py module.

    Attributes:
        test_dir (str): Directory for holding test files.
    """

    def set_up(self):
        """Set up test files before running unit tests."""
        self.test_dir = abspath(join(expanduser("~"), "renameFilesTest"))
        mkdir(self.test_dir)
        # DVK 1
        dvk = Dvk()
        dvk.set_file(join(self.test_dir, "d1.dvk"))
        dvk.set_id("ID123")
        dvk.set_title("Title 1")
        dvk.set_artist("artist")
        dvk.set_page_url("/url/")
        dvk.set_media_file("d1.txt")
        open(dvk.get_media_file(), "a").close()
        dvk.write_dvk()
        # DVK 2
        dvk.set_file(join(self.test_dir, "d2.dvk"))
        dvk.set_id("D2")
        dvk.set_title("Title 2")
        dvk.set_media_file("d2.txt")
        open(dvk.get_media_file(), "a").close()
        dvk.set_secondary_file("d2.png")
        open(dvk.get_secondary_file(), "a").close()
        dvk.write_dvk()

    def tear_down(self):
        """Delete test files after ErrorFinding testing."""
        rmtree(self.test_dir)

    def test_rename_files(self):
        """Test the rename_files function."""
        try:
            self.set_up()
            rename_files(self.test_dir)
            dvk_handler = DvkHandler()
            dvk_handler.load_dvks([self.test_dir])
            dvk_handler.sort_dvks("a")
            # DVK 1
            title = "Title 1_ID123.dvk"
            assert basename(dvk_handler.get_dvk_sorted(0).get_file()) == title
            assert exists(dvk_handler.get_dvk_sorted(0).get_file())
            title = "Title 1_ID123.txt"
            file = dvk_handler.get_dvk_sorted(0).get_media_file()
            assert basename(file) == title
            assert exists(dvk_handler.get_dvk_sorted(0).get_media_file())
            # DVK 2
            title = "Title 2_D2.dvk"
            assert basename(dvk_handler.get_dvk_sorted(1).get_file()) == title
            assert exists(dvk_handler.get_dvk_sorted(1).get_file())
            title = "Title 2_D2.txt"
            file = dvk_handler.get_dvk_sorted(1).get_media_file()
            assert basename(file) == title
            assert exists(dvk_handler.get_dvk_sorted(1).get_media_file())
            title = "Title 2_D2.png"
            file = basename(dvk_handler.get_dvk_sorted(1).get_secondary_file())
            assert file == title
            assert exists(dvk_handler.get_dvk_sorted(1).get_secondary_file())
            assert dvk_handler.get_size() == 2
        finally:
            self.tear_down()

    def run_all(self):
        """Test all functions of the rename_files.py module."""
        self.test_rename_files()
