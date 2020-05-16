# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pomace', 'pomace.tests']

package_data = \
{'': ['*']}

install_requires = \
['bullet>=2.1.0,<3.0.0',
 'cleo>=0.7.6,<0.8.0',
 'datafiles==0.10b1',
 'ipython>=7.12.0,<8.0.0',
 'minilog==1.6b5',
 'parse>=1.14.0,<2.0.0',
 'splinter>=0.12.0,<0.13.0',
 'webdriver_manager>=2.5.0,<3.0.0']

entry_points = \
{'console_scripts': ['pomace = pomace.cli:application.run']}

setup_kwargs = {
    'name': 'pomace',
    'version': '0.0.10',
    'description': 'Dynamic page objects for browser automation.',
    'long_description': '# Overview\n\nDynamic page objects for browser automation.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Unix Build Status](https://img.shields.io/travis/jacebrowning/pomace/develop.svg?label=unix)](https://travis-ci.org/jacebrowning/pomace)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/pomace/develop.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/pomace)\n[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/pomace/develop.svg)](https://coveralls.io/r/jacebrowning/pomace)\n[![PyPI Version](https://img.shields.io/pypi/v/pomace.svg)](https://pypi.org/project/pomace)\n[![PyPI License](https://img.shields.io/pypi/l/pomace.svg)](https://pypi.org/project/pomace)\n\n# Setup\n\n## Requirements\n\n- Python 3.8+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install pomace\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add pomace\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import pomace\n>>> pomace.__version__\n```\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pomace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
