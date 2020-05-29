# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['itarj_console']
entry_points = \
{'console_scripts': ['ItarjConsole_app = itarj_console:main']}

setup_kwargs = {
    'name': 'itarjconsole-app',
    'version': '1.0.0',
    'description': 'A console app that allows users to register fake job alerts and allows others to view those posts by searching for keywords.',
    'long_description': 'ItarjConsole (1.0.0)\n\npip install ItarjConsole\n\nAfter installation, type ItarjConsole_app to run the program',
    'author': 'Onuh Chukwuma',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
