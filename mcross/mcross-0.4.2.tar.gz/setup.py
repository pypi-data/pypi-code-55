# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mcross', 'mcross.gui']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mcross = mcross:run']}

setup_kwargs = {
    'name': 'mcross',
    'version': '0.4.2',
    'description': 'Do you remember www?',
    'long_description': None,
    'author': 'nhanb',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
