# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['open_link']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pobject>=0.1.5,<0.2.0', 'pyperclip>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['open-link = open_link.main:main']}

setup_kwargs = {
    'name': 'open-link',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Eyal Levin',
    'author_email': 'eyalev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
