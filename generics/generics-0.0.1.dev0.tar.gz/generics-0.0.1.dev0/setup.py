# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['generics']
setup_kwargs = {
    'name': 'generics',
    'version': '0.0.1.dev0',
    'description': '',
    'long_description': None,
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
