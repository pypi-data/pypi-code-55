# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tripod_lambda']
install_requires = \
['attrs>=19.3.0,<20.0.0',
 'boto3>=1.13.18,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['tripod = tripod_lambda:cli']}

setup_kwargs = {
    'name': 'tripod-lambda',
    'version': '0.1.0',
    'description': 'really lightweight scaffolding for lambda',
    'long_description': '# tripod\n\nreally lightweight scaffolding for AWS Lambda\n',
    'author': 'James Turk',
    'author_email': 'dev@jamesturk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
