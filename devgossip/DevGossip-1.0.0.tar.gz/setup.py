# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['devgossip']
entry_points = \
{'console_scripts': ['DevGossip = DevGossip:register_user']}

setup_kwargs = {
    'name': 'devgossip',
    'version': '1.0.0',
    'description': 'A simple discussion platform for social communication within the office',
    'long_description': None,
    'author': 'Abumere Ogona',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
