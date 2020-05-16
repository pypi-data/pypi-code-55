# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tooner']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tooner',
    'version': '1.0.1',
    'description': 'An easier way to manage and launch sessions for Toontown Rewritten.',
    'long_description': None,
    'author': 'Jake Brehm',
    'author_email': 'mail@jakebrehm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
