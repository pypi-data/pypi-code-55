# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['randalgo1']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['randalgo = randalgo:app']}

setup_kwargs = {
    'name': 'randalgo1',
    'version': '0.1.3',
    'description': 'a console app that fetches random question from public api',
    'long_description': None,
    'author': 'charles',
    'author_email': 'charlesclinton2003@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
