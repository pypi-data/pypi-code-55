# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['requestalgorithms', 'README', 'userplay']
entry_points = \
{'console_scripts': ['RandoAlgo = userplay:userLogin']}

setup_kwargs = {
    'name': 'randoalgo-rjay',
    'version': '0.1.0',
    'description': 'A python package that gets random algorithm questions',
    'long_description': None,
    'author': 'Rashidat Jimoh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
