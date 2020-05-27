# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airsupply']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'boto3>=1.11.8,<2.0.0',
 'click>=7.0,<8.0',
 'jinja2>=2.10.3,<3.0.0',
 'pyaxmlparser>=0.3.24,<0.4.0']

entry_points = \
{'console_scripts': ['airsupply = airsupply.cli:main']}

setup_kwargs = {
    'name': 'airsupply',
    'version': '0.2.5',
    'description': 'Manage OTA distribution for IPA and APK files.',
    'long_description': None,
    'author': 'Michael Merickel',
    'author_email': None,
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
