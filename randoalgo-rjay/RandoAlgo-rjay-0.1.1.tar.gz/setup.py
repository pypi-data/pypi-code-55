# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['requestalgorithms', 'README', 'userplay']
entry_points = \
{'console_scripts': ['RandoAlgo = userplay:userLogin']}

setup_kwargs = {
    'name': 'randoalgo-rjay',
    'version': '0.1.1',
    'description': 'A python package that gets random algorithm questions',
    'long_description': "<h1>Rando ALgo</h1>\nA python package that allows users to get random algorithm questions to practice. \n<h2>Usage</h2>\n<p>To use Rando Algo, user can install it as a pypi package.</p>\n<p>To install this package go to <a href= https://pypi.org/manage/projects/>alt='Link to RandoAlgo package</a>.\nYou can also run pip install randoalgo-rjay on your command line.</p>\n<p>To use app on Commandline, enter <b>RandoAlgo</b>\n<p>Users must have request and beautifulsoup4 libraries installed to use app<p>\n<p>Users have to have login and enter in a password, after this they can now enter a number to practice algorithm questions.</p>\n<p>User can play as many times as they want to but if they no longer wish to continue, they can exit.</p>\n",
    'author': 'Rashidat Jimoh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/startng/forward--RandoAlgo-Rjay',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
