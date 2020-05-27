# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapalgebra']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mapalgebra = mapalgebra.console:run']}

setup_kwargs = {
    'name': 'mapalgebra',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'chenn',
    'author_email': 'chenn@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
