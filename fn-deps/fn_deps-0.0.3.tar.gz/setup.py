# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fn_deps']
install_requires = \
['click>=7.1.2,<8.0.0',
 'dephell>=0.8.3,<0.9.0',
 'gitpython>=3.1.2,<4.0.0',
 'sh>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['fn_deps = fn_deps:cli']}

setup_kwargs = {
    'name': 'fn-deps',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@businessoptics.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BusinessOptics/fn_deps',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
