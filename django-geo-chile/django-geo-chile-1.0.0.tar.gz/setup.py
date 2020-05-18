# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geo_chile',
 'geo_chile.management',
 'geo_chile.management.commands',
 'geo_chile.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'django-geo-chile',
    'version': '1.0.0',
    'description': 'Region, Province and Commune populated django models.',
    'long_description': '# django-geo-chile',
    'author': 'Francisco Ceruti',
    'author_email': 'hello@fceruti.com',
    'maintainer': 'Francisco Ceruti',
    'maintainer_email': 'hello@fceruti.com',
    'url': 'https://github.com/fceruti/django-geo-chile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
