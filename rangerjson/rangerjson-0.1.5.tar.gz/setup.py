# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rangerjson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rangerjson',
    'version': '0.1.5',
    'description': '',
    'long_description': '# README\n\nInteract with Ranger json dump from api\n\n## Ranger model\n\n![overview](img/ranger-general.png)\n\nEach policies has a number of similarties with each other but have some specialities (hdf path ...)\n\n![policies](img/ranger-policies.png)\n',
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
