#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Vanessa Daza,
#                     Juan B Cabral, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Utilities to access different Argentina-Related databases of
COVID-19 data from the Arcovid19 group.

"""


# =============================================================================
# IMPORTS
# =============================================================================

import pathlib
import os

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages  # noqa


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

REQUIREMENTS = [
    "numpy", "pandas", "clize", "diskcache",
    "xlrd", "attrs", "deprecated",
    "Flask", "Flask-WTF", "numpydoc", "openpyxl", "mpld3",
    "flask_babel", "matplotlib", "seaborn"]


with open(PATH / "README.rst") as fp:
    LONG_DESCRIPTION = fp.read()


DESCRIPTION = (
    "Utilities to access different Argentina-Related databases of "
    "COVID-19 data from the IATE task force.")


with open(PATH / "arcovid19" / "__init__.py") as fp:
    VERSION = [
        line for line in fp.readlines() if line.startswith("__version__")
    ][0].split("=", 1)[-1].strip().replace('"', "")


# =============================================================================
# FUNCTIONS
# =============================================================================

def do_setup():
    setup(
        name="arcovid19",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author="IATE COVID-19 Task Force",
        author_email="jbc.develop@gmail.com",
        url="https://github.com/ivco19/libs",
        license="BSD-3",
        keywords=["covid-19", "project", "datasets", "argentina"],
        classifiers=(
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering"),
        py_modules=["ez_setup"],
        packages=["arcovid19", "arcovid19.web"],
        entry_points={
            'console_scripts': ['arcovid19=arcovid19.cli:main']},
        install_requires=REQUIREMENTS,
        include_package_data=True)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    do_setup()
