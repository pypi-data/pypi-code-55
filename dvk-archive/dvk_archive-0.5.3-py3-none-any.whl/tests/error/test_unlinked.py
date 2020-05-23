#!/usr/bin/env python3

"""Unit tests for the unlinked.py module."""

from shutil import rmtree
from os import mkdir
from os.path import abspath, basename, expanduser, join
from dvk_archive.file.dvk import Dvk
from dvk_archive.file.dvk_handler import DvkHandler
from dvk_archive.error.unlinked import unlinked_media


class TestUnlinkedMedia():
    """
    Unit tests for the unlinked.py module.

    Attributes:
        test_dir (str): Directory for holding test files.
    """

    def set_up(self):
        """Set up test files before running unit tests."""
        self.test_dir = abspath(join(expanduser("~"), "findingTest"))
        mkdir(self.test_dir)
        open(join(self.test_dir, "file0"), "a").close()
        sub = join(self.test_dir, "sub")
        mkdir(sub)
        sub2 = join(self.test_dir, "sub2")
        mkdir(sub2)
        # CREATE UNLINKED FILE
        file = join(sub2, "noDVK.txt")
        open(file, "a").close()
        # DVK 1
        dvk = Dvk(join(self.test_dir, "dvk1.dvk"))
        file = join(self.test_dir, "file1.txt")
        open(file, "a").close()
        dvk.set_id("id1")
        dvk.set_title("title1")
        dvk.set_artist("artist")
        dvk.set_page_url("/page/url")
        dvk.set_media_file(file)
        file = join(self.test_dir, "fileSecond.no")
        open(file, "a").close()
        dvk.set_secondary_file(file)
        dvk.write_dvk()
        # DVK 2
        file = join(sub, "file2.png")
        open(file, "a").close()
        dvk.set_id("id2")
        dvk.set_title("title2")
        dvk.set_file(join(sub, "dvk2.dvk"))
        dvk.set_media_file(file)
        file = join(sub, "second.dmf")
        dvk.set_secondary_file(file)
        dvk.write_dvk()
        # DVK 3
        open(join(sub, "file1.txt"), "a").close()
        file = join(sub, "file3.svg")
        dvk.set_id("id1")
        dvk.set_title("title3")
        dvk.set_file(join(sub, "dvk3.dvk"))
        dvk.set_media_file(file)
        dvk.set_secondary_file(None)
        dvk.write_dvk()
        # DVK 4
        file = join(self.test_dir, "file4.ogg")
        dvk.set_title("title4")
        dvk.set_file(join(self.test_dir, "dvk4.dvk"))
        dvk.set_media_file(file)
        dvk.write_dvk()

    def tear_down(self):
        """Delete test files after ErrorFinding testing."""
        rmtree(self.test_dir)

    def test_unlinked_media(self):
        """Test the unlinked_media function."""
        try:
            self.set_up()
            missing = unlinked_media([self.test_dir])
            assert len(missing) == 2
            assert basename(missing[0]) == "file0"
            assert basename(missing[1]) == "file1.txt"
            assert unlinked_media() == []
            handler = DvkHandler()
            handler.load_dvks([join(self.test_dir, "sub")])
            missing = unlinked_media(dvk_handler=handler)
            assert len(missing) == 1
            assert basename(missing[0]) == "file1.txt"
        finally:
            self.tear_down()

    def run_all(self):
        """Test all functions of the unlinked.py module."""
        self.test_unlinked_media()
