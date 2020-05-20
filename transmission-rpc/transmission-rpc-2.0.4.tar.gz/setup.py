# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transmission_rpc']

package_data = \
{'': ['*']}

install_requires = \
['requests']

extras_require = \
{'docs': ['sphinx>=2.2,<3.0',
          'sphinx-rtd-theme>=0.4.3,<0.5.0',
          'sphinx-issues==1.2.0']}

setup_kwargs = {
    'name': 'transmission-rpc',
    'version': '2.0.4',
    'description': 'Python module that implements the Transmission bittorent client RPC protocol',
    'long_description': '# Transmission-rpc Readme\n\nthis project is forked from https://bitbucket.org/blueluna/transmissionrpc/overview\n\n## Introduction\n\n`transmission-rpc` is a python module implementing the json-rpc client protocol for the BitTorrent client Transmission.\n\n## Requirements\n\ntransmission_rpc requires:\n\n* Python >= 3.4\n* requests\n\n## Install\n\n### install from pypi\n\n```bash\n$ pip install transmission-rpc\n```\n\n### install from source\n\n```bash\n$ pip install https://github.com/Trim21/transmission-rpc/tarball/master\n```\n\nNOTE: You might need administrator privileges to install python modules.\n\n<!-- The setup program will take care of the simple json requirement. -->\n\n## Documents\n\n<https://transmission-rpc.readthedocs.io/>\n\n## Break change\n\n## Developer\n\ntransmission-rpc is hosted by GitHub at [github.com/Trim21/transmission-rpc](https://github.com/Trim21/transmission-rpc)\n\n`transmission-rpc` is licensed under the MIT license.\n\nCopyright (c) 2018 Trim21.\nCopyright (c) 2008-2014 Erik Svensson\n',
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Trim21/transmission-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
