# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['main', 'utils', 'README']
entry_points = \
{'console_scripts': ['dev-gossip = main:runapp']}

setup_kwargs = {
    'name': 'devgossip-praiseey',
    'version': '0.1.0',
    'description': 'Gossip platform for any topic for developers.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
