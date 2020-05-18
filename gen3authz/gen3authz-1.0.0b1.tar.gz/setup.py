# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gen3authz', 'gen3authz.client', 'gen3authz.client.arborist']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.6,<2.0',
 'cdiserrors>=1.0.0-beta.1,<2.0.0',
 'httpx>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'gen3authz',
    'version': '1.0.0b1',
    'description': 'Gen3 authz client',
    'long_description': None,
    'author': 'CTDS UChicago',
    'author_email': 'cdis@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
