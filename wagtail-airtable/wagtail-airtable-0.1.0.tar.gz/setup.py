# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_airtable',
 'wagtail_airtable.management.commands',
 'wagtail_airtable.migrations']

package_data = \
{'': ['*'], 'wagtail_airtable': ['templates/wagtail_airtable/*']}

install_requires = \
['airtable-python-wrapper>=0.13.0,<0.14.0',
 'djangorestframework>=3.11.0,<3.12.0']

setup_kwargs = {
    'name': 'wagtail-airtable',
    'version': '0.1.0',
    'description': 'Sync data between Wagtail and Airtable',
    'long_description': None,
    'author': 'Kalob Taulien',
    'author_email': 'kalob.taulien@torchbox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
