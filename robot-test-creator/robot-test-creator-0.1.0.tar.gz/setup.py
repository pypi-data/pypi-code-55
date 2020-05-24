# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robot_test_creator']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'rpa-framework>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['rtc = robot_test_creator.excel2suites:main']}

setup_kwargs = {
    'name': 'robot-test-creator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mika Hänninen',
    'author_email': 'mika@robocorp.com',
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
