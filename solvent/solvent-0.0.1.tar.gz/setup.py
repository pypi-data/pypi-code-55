# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solvent']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.0.3,<5.0.0', 'pomace==0.0.11']

entry_points = \
{'console_scripts': ['solvent = solvent:main']}

setup_kwargs = {
    'name': 'solvent',
    'version': '0.0.1',
    'description': 'Kills off fake grass.',
    'long_description': None,
    'author': 'Solvent',
    'author_email': 'solvent@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
