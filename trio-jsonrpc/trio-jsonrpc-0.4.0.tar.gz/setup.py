# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trio_jsonrpc', 'trio_jsonrpc.transport']

package_data = \
{'': ['*']}

install_requires = \
['sansio-jsonrpc>=0.2.0,<0.3.0', 'trio-websocket>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'trio-jsonrpc',
    'version': '0.4.0',
    'description': 'JSON-RPC v2.0 for Trio',
    'long_description': "# JSON-RPC v2.0 for Trio\n\n[![PyPI](https://img.shields.io/pypi/v/trio-jsonrpc.svg?style=flat-square)](https://pypi.org/project/trio-jsonrpc/)\n![Python Versions](https://img.shields.io/pypi/pyversions/trio-jsonrpc.svg?style=flat-square)\n![MIT License](https://img.shields.io/github/license/HyperionGray/trio-jsonrpc.svg?style=flat-square)\n[![Build Status](https://img.shields.io/travis/com/HyperionGray/trio-jsonrpc.svg?style=flat-square&branch=master)](https://travis-ci.com/HyperionGray/trio-jsonrpc)\n[![codecov](https://img.shields.io/codecov/c/github/hyperiongray/trio-jsonrpc?style=flat-square)](https://codecov.io/gh/HyperionGray/trio-jsonrpc)\n[![Read the Docs](https://img.shields.io/readthedocs/trio-jsonrpc.svg)](https://trio-jsonrpc.readthedocs.io)\n\nThis project provides an implementation of [JSON-RPC v\n2.0](https://www.jsonrpc.org/specification) based on\n[sansio-jsonrpc](https://github.com/hyperiongray/sansio-jsonrpc) with all of the I/O\nimplemented using the [Trio asynchronous framework](https://trio.readthedocs.io).\n\n## Quick Start\n\nInstall from PyPI:\n\n```\n$ pip install trio-jsonrpc\n```\n\nThe following example shows a basic JSON-RPC client.\n\n```python\nfrom trio_jsonrpc import open_jsonrpc_ws, JsonRpcException\n\nasync def main():\n    async with open_jsonrpc_ws('ws://example.com/') as client:\n        try:\n            result = await client.request(\n                method='open_vault_door',\n                {'employee': 'Mark', 'pin': 1234}\n            )\n            print('vault open:', result['vault_open'])\n\n            await client.notify(method='hello_world')\n        except JsonRpcException as jre:\n            print('RPC failed:', jre)\n\ntrio.run(main)\n```\n\nFor more information, see [the complete\ndocumentation](https://trio-jsonrpc.readthedocs.io).\n",
    'author': 'Mark E. Haase',
    'author_email': 'mehaase@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hyperiongray/trio-jsonrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
