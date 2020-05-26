# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.odf', 'berhoel.odf.test']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.5.0,<5.0.0', 'pdoc3>=0.8.1,<0.9.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'berhoelodf',
    'version': '0.1.3',
    'description': 'Lightweight and limited access to odf files using lxml.',
    'long_description': '# berhoelODF\n\nLightweight and limited access to odf files using lxml.',
    'author': 'Berthold Höllmann',
    'author_email': 'berthold-gitlab@xn--hllmanns-n4a.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python.xn--hllmanns-n4a.de/berhoelodf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
