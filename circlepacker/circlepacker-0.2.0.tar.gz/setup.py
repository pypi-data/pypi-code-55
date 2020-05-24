# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['circlepacker',
 'circlepacker.domain',
 'circlepacker.optimization',
 'circlepacker.routers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.54.2,<0.55.0',
 'pydantic>=1.5.1,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'uvicorn>=0.11.5,<0.12.0']

setup_kwargs = {
    'name': 'circlepacker',
    'version': '0.2.0',
    'description': 'A service for computing circle packing',
    'long_description': '# circle-packer\n\n## Why pack circles?\n\n## How to use\n\n## Routing ',
    'author': "Ryan O'Sullivan",
    'author_email': 'osullivryan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/osullivryan/circle-packer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
