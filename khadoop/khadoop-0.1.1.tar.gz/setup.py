# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khadoop', 'khadoop.yarn']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'khadoop',
    'version': '0.1.1',
    'description': '',
    'long_description': '# README\n\nParse and slice hadoop logs\n',
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
