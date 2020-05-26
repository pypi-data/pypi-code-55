# This file is managed by `git_helper`. Don't edit it directly
# Copyright (C) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This script based on https://github.com/rocky/python-uncompyle6/blob/master/__pkginfo__.py

import pathlib

__all__ = [
		"__copyright__",
		"__version__",
		"modname",
		"pypi_name",
		"py_modules",
		"entry_points",
		"__license__",
		"short_desc",
		"author",
		"author_email",
		"github_username",
		"web",
		"github_url",
		"project_urls",
		"repo_root",
		"long_description",
		"install_requires",
		"extras_require",
		"classifiers",
		"keywords",
		"import_name",
		]

__copyright__ = """
2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

__version__ = "0.3.0"

modname = "chemistry_tools"
pypi_name = "chemistry_tools"
import_name = "chemistry_tools"
py_modules = []
entry_points = {
		"console_scripts": []
		}

__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"

short_desc = "Python tools for analysis of chemical compounds"

__author__ = author = "Dominic Davis-Foster"
author_email = "dominic@davis-foster.co.uk"
github_username = "domdfcoding"
web = github_url = f"https://github.com/domdfcoding/chemistry_tools"
project_urls = {
		"Documentation": f"https://chemistry_tools.readthedocs.io",  # TODO: Make this link match the package version
		"Issue Tracker": f"{github_url}/issues",
		"Source Code": github_url,
		}

repo_root = pathlib.Path(__file__).parent

# Get info from files; set: long_description
long_description = (repo_root / "README.rst").read_text().replace("0.3.0", __version__) + '\n'
conda_description = """Python tools for analysis of chemical compounds


Before installing please ensure you have added the following channels: domdfcoding, conda-forge"""
__all__.append("conda_description")

install_requires = (repo_root / "requirements.txt").read_text().split('\n')
extras_require = {'pubchem': ['tabulate>=0.8.3', 'pandas>=1.0.1', 'memoized-property>=1.0.3', 'domdf_python_tools>=0.3.3', 'Pillow>=7.0.0'], 'elements': ['domdf_python_tools>=0.3.3', 'memoized-property>=1.0.3'], 'formulae': ['quantities>=0.12.4', 'domdf_python_tools>=0.3.3', 'tabulate>=0.8.3', 'pyparsing>=2.2.0', 'pandas>=1.0.1', 'mathematical>=0.1.7', 'cawdrey>=0.1.2', 'memoized-property>=1.0.3'], 'plotting': ['matplotlib>=3.0.0'], 'toxnet': ['beautifulsoup4>=4.7.0'], 'all': ['Pillow>=7.0.0', 'beautifulsoup4>=4.7.0', 'cawdrey>=0.1.2', 'domdf_python_tools>=0.3.3', 'mathematical>=0.1.7', 'matplotlib>=3.0.0', 'memoized-property>=1.0.3', 'pandas>=1.0.1', 'pyparsing>=2.2.0', 'quantities>=0.12.4', 'tabulate>=0.8.3']}

classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Database :: Front-Ends',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'Topic :: Scientific/Engineering :: Chemistry',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3 :: Only',
		'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

		]

keywords = ""
