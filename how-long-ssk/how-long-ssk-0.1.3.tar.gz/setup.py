# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['how_long_ssk']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'how-long-ssk',
    'version': '0.1.3',
    'description': 'Example from https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-3/. A simple decorator to measure a function execution time',
    'long_description': None,
    'author': 'Stephen Kelley',
    'author_email': 'skelley@unitedlife.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
