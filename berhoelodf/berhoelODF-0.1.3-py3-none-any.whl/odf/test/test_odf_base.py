#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing base functionalities of berhoel.odf library.
"""

# Standard libraries.
from pathlib import Path

# Third party libraries.
import toml
import pytest

from berhoel.odf import Odf, __version__

__date__ = "2020/05/26 22:35:33 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


@pytest.fixture
def py_project(base_path):
    "Return path of project `pyproject.toml`."
    return base_path / "pyproject.toml"


@pytest.fixture
def toml_inst(py_project):
    "Return `toml` instance of project `pyproject.toml`"
    return toml.load(py_project.open("r"))


def test_version(toml_inst):
    "Test for consistent version numbers."
    assert __version__ == toml_inst["tool"]["poetry"]["version"]


def test_init(data1):
    _ = Odf(data1)


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
