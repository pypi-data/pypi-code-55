# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['devgossip', 'readme', 'requirements']
install_requires = \
['pusher>=3.0.0,<4.0.0', 'pysher>=1.0.6,<2.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['devgossip_v2 = devgossip:gossip']}

setup_kwargs = {
    'name': 'devgossip-v2',
    'version': '2.2.5',
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
