#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Common settiongs for testing `berhoel.odf`.
"""
# Standard libraries.
from pathlib import Path

# Third party libraries.
import pytest

__date__ = "2020/05/26 22:36:47 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


@pytest.fixture
def base_path():
    "Return path to project base."
    return Path(__file__).parents[3]


@pytest.fixture
def data_path(base_path):
    "Return path to data directory."
    return base_path / "data"


@pytest.fixture
def data1(data_path):
    "Return path to first sample data file."
    return data_path / "sample1.ods"


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
