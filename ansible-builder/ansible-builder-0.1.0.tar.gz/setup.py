# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansible_builder']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['ansible-builder = ansible_builder.cli:run']}

setup_kwargs = {
    'name': 'ansible-builder',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matthew Jones',
    'author_email': 'matburt@redhat.com',
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
