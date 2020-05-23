#!/usr/bin/env python3

"""Combined unit tests for the reformat package."""

from dvk_archive.tests.reformat.test_rename_files import TestRenameFiles


def test_reformat():
    """Run all reformat tests."""
    test_rename_files = TestRenameFiles()
    test_rename_files.run_all()
