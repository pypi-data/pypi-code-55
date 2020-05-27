# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notion_backup']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'prompt_toolkit>=3.0.5,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'notion-backup',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Hugo Lime',
    'author_email': 'ligohu@outlook.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.2',
}


setup(**setup_kwargs)
