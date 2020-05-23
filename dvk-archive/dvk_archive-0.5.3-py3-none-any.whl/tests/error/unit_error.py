#!/usr/bin/env python3

"""Combined unit tests for the error package."""

from dvk_archive.tests.error.test_missing_media import TestMissingMedia
from dvk_archive.tests.error.test_same_ids import TestSameIDs
from dvk_archive.tests.error.test_unlinked import TestUnlinkedMedia


def test_error():
    """Run all error tests."""
    same_ids = TestSameIDs()
    unlinked = TestUnlinkedMedia()
    missing_media = TestMissingMedia()
    same_ids.run_all()
    unlinked.run_all()
    missing_media.run_all()
