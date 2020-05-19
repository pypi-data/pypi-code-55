# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['biip']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'biip',
    'version': '0.1.0',
    'description': 'Biip interprets the data in barcodes.',
    'long_description': '# Biip\n\nBiip interprets the data in barcodes.\n\n[![Tests](https://github.com/jodal/biip/workflows/Tests/badge.svg)](https://github.com/jodal/biip/actions?workflow=Tests)\n[![PyPI](https://img.shields.io/pypi/v/biip.svg)](https://pypi.org/project/biip/)\n',
    'author': 'Stein Magnus Jodal',
    'author_email': 'stein.magnus@jodal.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jodal/biip',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
