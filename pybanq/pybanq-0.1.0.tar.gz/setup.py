# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybanq',
 'pybanq.asi',
 'pybanq.asi.block',
 'pybanq.block',
 'pybanq.nano',
 'pybanq.nano.asi',
 'pybanq.nano.asi.block',
 'pybanq.nano.block',
 'pybanq.quantum',
 'pybanq.quantum.asi',
 'pybanq.quantum.asi.block',
 'pybanq.quantum.block',
 'pybanq.quantum.nano',
 'pybanq.quantum.nano.asi',
 'pybanq.quantum.nano.asi.block',
 'pybanq.quantum.nano.block']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybanq',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jachiike Madubuko',
    'author_email': 'jachiike.madubuko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
