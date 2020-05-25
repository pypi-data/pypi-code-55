# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['influp']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['influp = influp.influp:main']}

setup_kwargs = {
    'name': 'influp',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Viet Nguyen',
    'author_email': 'me@tuanviet.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
