# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wmg_tool']

package_data = \
{'': ['*']}

install_requires = \
['instaloader>=4.4.3,<5.0.0', 'instalooter>=2.4.2,<3.0.0']

setup_kwargs = {
    'name': 'wmg-tool',
    'version': '0.1.0',
    'description': 'grab content pictures or  videos from social media',
    'long_description': None,
    'author': 'wongselent',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
