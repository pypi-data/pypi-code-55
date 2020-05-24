# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rotations']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

setup_kwargs = {
    'name': 'rotations',
    'version': '0.0.1',
    'description': 'Reference frame rotation sequences',
    'long_description': '# Rotations\n\n**Under construction**\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/rotations/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
