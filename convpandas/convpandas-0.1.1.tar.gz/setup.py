# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convpandas', 'convpandas.command']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['convpandas = convpandas.__main__:cli']}

setup_kwargs = {
    'name': 'convpandas',
    'version': '0.1.1',
    'description': 'Convert file format with pandas',
    'long_description': '# convert-fileformat-with-pandas\nConvert file format with pandas\n\n[![Build Status](https://travis-ci.org/yuji38kwmt/convpandas.svg?branch=master)](https://travis-ci.org/yuji38kwmt/convpandas)\n[![PyPI version](https://badge.fury.io/py/convpandas.svg)](https://badge.fury.io/py/convpandas)\n[![Python Versions](https://img.shields.io/pypi/pyversions/convpandas.svg)](https://pypi.org/project/convpandas/)\n\n# Requirements\n* Python 3.6+\n\n# Install\n\n```\n$ pip install convpandas\n```\n\nhttps://pypi.org/project/convpandas/\n\n\n# Usage\n\n## csv2xlsx\nConvert csv file to xlsx file.\n\n```\n$ convpandas csv2xlsx in.csv out.xlsx\n```\n\n### Options\n\n```\nOptions:\n  --sep TEXT                   Delimiter to use when reading csv.  [default:,]\n  --encoding TEXT              Encoding to use when reading csv. List of Python standard encodings .  [default: utf-8]\n  --quotechar TEXT             The character used to denote the start and end of a quoted item when reading csv.\n  --string_to_numeric BOOLEAN  If true, convert string to numeric. [default: utf-8]\n```\n\n## xlsx2csv\nConvert xlsx file to csv file.\n\n```\n$ convpandas xlsx2csv in.xlsx out.csv\n```\n\n\n```\nOptions:\n  --sheet_name TEXT  Sheet name when reading xlsx. If not specified, read 1st sheet.\n  --sep TEXT         Field delimiter for the output file.  [default: ,]\n  --encoding TEXT    A string representing the encoding to use in the output file.  [default: utf-8]\n  --quotechar TEXT   Character used to quote fields.\n```\n',
    'author': 'yuji38kwmt',
    'author_email': 'yuji38kwmt@yahoo.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuji38kwmt/convert-fileformat-with-pandas.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
