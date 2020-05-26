# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigbluebutton',
 'bigbluebutton.api',
 'bigbluebutton.cli',
 'bigbluebutton.django',
 'bigbluebutton.django.migrations']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.3.2,<0.4.0',
 'inflection>=0.4.0,<0.5.0',
 'requests>=2.23.0,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

extras_require = \
{'cli': ['click>=7.1.1,<8.0.0',
         'toml>=0.10.0,<0.11.0',
         'tabulate>=0.8.7,<0.9.0'],
 'django': ['django>=3.0.6,<4.0.0'],
 'sysstat': ['sadf>=0.1.2,<0.2.0']}

entry_points = \
{'console_scripts': ['bbb-cli = bigbluebutton.cli:bbb']}

setup_kwargs = {
    'name': 'bigbluebutton2',
    'version': '0.1.0.dev0',
    'description': 'API client for BigBlueButton 2.0+',
    'long_description': None,
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://edugit.org/AlekSIS/libs/python-bigbluebutton2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
