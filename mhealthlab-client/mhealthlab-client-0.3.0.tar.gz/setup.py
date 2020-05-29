# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mhealthlab_client']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'loguru>=0.4.1,<0.5.0',
 'pandas>=1.0.3,<2.0.0',
 'paramiko>=2.7.1,<3.0.0',
 'progress>=1.5,<2.0',
 'pyzipper>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['mhlab = mhealthlab_client.mhlab:mhlab']}

setup_kwargs = {
    'name': 'mhealthlab-client',
    'version': '0.3.0',
    'description': 'Client to download and decrypt data for lab projects of mhealthgroup.org',
    'long_description': None,
    'author': 'Qu Tang',
    'author_email': 'tang.q@northeastern.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
