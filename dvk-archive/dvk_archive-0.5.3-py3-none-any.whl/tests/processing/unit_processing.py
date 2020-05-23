#!/usr/bin/env python3

"""Combined unit tests of the processing package."""

from dvk_archive.tests.processing.test_html_processing import run_all as ht_p
from dvk_archive.tests.processing.test_list_processing import run_all as ls_p
from dvk_archive.tests.processing.test_printing import run_all as ts_p
from dvk_archive.tests.processing.test_string_compare import run_all as sc_p
from dvk_archive.tests.processing.test_string_processing import run_all as sp


def test_processing():
    """Run all processing tests."""
    ht_p()
    ls_p()
    ts_p()
    sc_p()
    sp()
