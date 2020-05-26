# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytile']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'pytile',
    'version': '3.0.5',
    'description': 'A simple Python API for Tile® Bluetooth trackers',
    'long_description': '# 📡 pytile: A simple Python API for Tile® Bluetooth trackers\n\n[![CI](https://github.com/bachya/pytile/workflows/CI/badge.svg)](https://github.com/bachya/pytile/actions)\n[![PyPi](https://img.shields.io/pypi/v/pytile.svg)](https://pypi.python.org/pypi/pytile)\n[![Version](https://img.shields.io/pypi/pyversions/pytile.svg)](https://pypi.python.org/pypi/pytile)\n[![License](https://img.shields.io/pypi/l/pytile.svg)](https://github.com/bachya/pytile/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/pytile/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/pytile)\n[![Maintainability](https://api.codeclimate.com/v1/badges/71eb642c735e33adcdfc/maintainability)](https://codeclimate.com/github/bachya/pytile/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\n`pytile` is a simple Python library for retrieving information on\n[Tile® Bluetooth trackers](https://www.thetileapp.com/en-us/) (including last\nlocation and more).\n\nThis library is built on an unpublished, unofficial Tile API; it may alter or\ncease operation at any point.\n\n- [Python Versions](#python-versions)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Contributing](#contributing)\n\n# Python Versions\n\n`pytile` is currently supported on:\n\n* Python 3.6\n* Python 3.7\n* Python 3.8\n\n# Installation\n\n```python\npip install pytile\n```\n\n# Usage\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom pytile import async_login\n\n\nasync def main() -> None:\n    """Run!"""\n    client = await async_login("<EMAIL>", "<PASSWORD>")\n\n    # Get all Tiles associated with an account:\n    await client.tiles.all()\n\n\nasyncio.run(main())\n```\n\nBy default, the library creates a new connection to Tile with each coroutine. If you are\ncalling a large number of coroutines (or merely want to squeeze out every second of\nruntime savings possible), an\n[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection\npooling:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom pytile import async_login\n\n\nasync def main() -> None:\n    """Run!"""\n    async with ClientSession() as session:\n        client = await async_login("<EMAIL>", "<PASSWORD>", session)\n\n        # Get all Tiles associated with an account:\n        await client.tiles.all()\n\n\nasyncio.run(main())\n```\n\nIf for some reason you need to use a specific client UUID (to, say, ensure that the\nTile API sees you as a client it\'s seen before) or a specific locale, you can do\nso easily:\n\n```python\nimport asyncio\n\nfrom aiohttp import ClientSession\n\nfrom pytile import async_login\n\n\nasync def main() -> None:\n    """Run!"""\n    client = await async_login(\n        "<EMAIL>", "<PASSWORD>", client_uuid="MY_UUID", locale="en-GB"\n    )\n\n    # Get all Tiles associated with an account:\n    await client.tiles.all()\n\n\nasyncio.run(main())\n```\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/pytile/issues)\n  or [initiate a discussion on one](https://github.com/bachya/pytile/issues/new).\n2. [Fork the repository](https://github.com/bachya/pytile/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/pytile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
