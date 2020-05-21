# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_asgi_server']

package_data = \
{'': ['*']}

install_requires = \
['asgi-lifespan>=1.0.0,<2.0.0',
 'httpx>=0.12.1,<0.13.0',
 'pytest-asyncio>=0.10.0,<0.11.0',
 'pytest-xprocess>=0.13.1,<0.14.0',
 'pytest>=5.4.1,<6.0.0',
 'uvicorn>=0.11.3,<0.12.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0',
                             'websockets>=8,<9']}

setup_kwargs = {
    'name': 'pytest-asgi-server',
    'version': '0.2.0',
    'description': 'Convenient ASGI client/server fixtures for Pytest',
    'long_description': '<h1 align="center">pytest-asgi-server</h1>\n<h3 align="center">Convenient ASGI client/server fixtures for Pytest</h3>\n<p align="center">\n<a href="https://github.com/garytyler/pytest-asgi-server/actions">\n  <img alt="Actions Status" src="https://github.com/garytyler/pytest-asgi-server/workflows/tests/badge.svg">\n</a>\n<a href="https://codecov.io/gh/garytyler/pytest-asgi-server">\n  <img src="https://codecov.io/gh/garytyler/pytest-asgi-server/branch/master/graph/badge.svg?token=q7mUlqR3jF" />\n</a>\n<a href="https://pypi.org/project/pytest-asgi-server/">\n  <img alt="PyPI" src="https://img.shields.io/pypi/v/pytest-asgi-server">\n</a>\n<a href="https://pypi.org/project/pytest-asgi-server/">\n  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pytest-asgi-server">\n</a>\n<img alt="GitHub" src="https://img.shields.io/github/license/garytyler/pytest-asgi-server">\n<a href="https://github.com/psf/black">\n  <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n</a>\n</p>\n\n### NOTE: This is a beta product\n',
    'author': 'Gary Tyler',
    'author_email': 'mail@garytyler.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garytyler/pytest-asgi-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
