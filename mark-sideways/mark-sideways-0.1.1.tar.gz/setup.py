# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mark_sideways']

package_data = \
{'': ['*']}

install_requires = \
['rich>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['mark = mark_sideways.cli:mark']}

setup_kwargs = {
    'name': 'mark-sideways',
    'version': '0.1.1',
    'description': 'Render markdown in the terminal',
    'long_description': '# mark-sideways\n\n[![PyPI Version](https://img.shields.io/pypi/v/mark-sideways.svg)](https://pypi.org/project/mark-sideways/)\n![License](https://img.shields.io/pypi/l/mark-sideways.svg)\n![Python Support](https://img.shields.io/pypi/pyversions/mark-sideways.svg)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nRender markdown in the terminal\n\n```sh\nmark up example.md        # display markdown code rendered\nmark down example.md      # display markdown code with syntax highlighting\nmark sideways example.md  # display code and markdown side-by-side\n```\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chris48s/mark-sideways',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
