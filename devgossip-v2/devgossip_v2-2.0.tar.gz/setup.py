# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['devgossip', 'readme']
install_requires = \
['dotenv>=0.0.5,<0.0.6',
 'getpass>=1.2,<2.0',
 'json>=0.1.0,<0.2.0',
 'os>=0.1.2,<0.2.0',
 'pusher>=3.0.0,<4.0.0',
 'pysher>=1.0.6,<2.0.0',
 'random>=1.0.1,<2.0.0',
 're>=0.2.24,<0.3.0',
 'string>=0.50,<0.51',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['devgossip_v2 = devgossip:main']}

setup_kwargs = {
    'name': 'devgossip-v2',
    'version': '2.0',
    'description': 'Chat forum for interaction between developers',
    'long_description': None,
    'author': 'Mark Okhakumhe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
