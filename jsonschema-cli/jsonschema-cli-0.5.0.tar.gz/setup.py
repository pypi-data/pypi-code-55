# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_cli', 'jsonschema_cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['jsonschema-cli = jsonschema_cli.cli:run']}

setup_kwargs = {
    'name': 'jsonschema-cli',
    'version': '0.5.0',
    'description': 'A thin wrapper over [Python Jsonschema](https://github.com/Julian/jsonschema) to allow validating shcemas easily using simple CLI commands.',
    'long_description': None,
    'author': 'Eyal Mor',
    'author_email': 'eyalmor94@gmail.com',
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
