# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bmi_demo']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.2.1,<0.3.0']

entry_points = \
{'console_scripts': ['bmi_demo = bmi_demo.cli:main']}

setup_kwargs = {
    'name': 'bmi-demo',
    'version': '1.0.0',
    'description': 'A simple demo application to demonstrate how to use Poetry and Typer to create executable Python CLIs.',
    'long_description': None,
    'author': 'JoaoGFarias',
    'author_email': 'joao@thatsabug.com',
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
