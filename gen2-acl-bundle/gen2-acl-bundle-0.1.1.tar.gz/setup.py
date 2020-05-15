# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gen2aclbundle']

package_data = \
{'': ['*'],
 'gen2aclbundle': ['_config/*',
                   'acl/*',
                   'acl/check/*',
                   'acl/export/*',
                   'acl/set/*',
                   'client/*']}

install_requires = \
['azure-storage-file-datalake==12.0.0',
 'console-bundle>=0.2.0,<0.3.0',
 'pandas>=0.25.0,<0.26.0',
 'pyfony-bundles>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gen2-acl-bundle',
    'version': '0.1.1',
    'description': 'Azure DataLake ACL setup bundle for the Pyfony Framework',
    'long_description': 'Azure DataLake ACL setup bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/gen2-acl-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
