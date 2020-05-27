# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfcopy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfcopy',
    'version': '0.1.0',
    'description': 'Provides high-level functionality on the filesystem.',
    'long_description': '# pyfcopy\n\ntbd\n',
    'author': 'Arne Groskurth',
    'author_email': 'arne.groskurth@gears9.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arnegroskurth/pyfcopy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
