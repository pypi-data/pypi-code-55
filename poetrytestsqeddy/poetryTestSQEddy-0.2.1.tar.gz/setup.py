# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetrytestsqeddy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0']

entry_points = \
{'console_scripts': ['run = testEddySemQuest.py']}

setup_kwargs = {
    'name': 'poetrytestsqeddy',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Eddy Ferrara Jr.',
    'author_email': 'e.ferrara@semquest.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
