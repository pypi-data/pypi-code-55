# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['teal_lang',
 'teal_lang.cli',
 'teal_lang.controllers',
 'teal_lang.examples',
 'teal_lang.executors',
 'teal_lang.machine',
 'teal_lang.run',
 'teal_lang.teal_compiler',
 'teal_lang.teal_parser']

package_data = \
{'': ['*']}

install_requires = \
['docopt',
 'graphviz>=0.13.2,<0.14.0',
 'pydot>=1.4.1,<2.0.0',
 'pynamodb',
 'pyyaml>=5.3.1,<6.0.0',
 'schema>=0.7.2,<0.8.0',
 'sly>=0.4,<0.5']

entry_points = \
{'console_scripts': ['teal = teal_lang.cli.main:main']}

setup_kwargs = {
    'name': 'teal-lang',
    'version': '0.2.0',
    'description': 'The Teal Programming Language',
    'long_description': '## The Teal Programming Language\n\n![Tests](https://github.com/condense9/teal-lang/workflows/Build/badge.svg?branch=master) [![PyPI](https://badge.fury.io/py/teal-lang.svg)](https://pypi.org/project/teal-lang)\n\nTeal is a programming language for microservice orchestration. With it, you can \n- get "bare-metal" concurrency on AWS Lambda\n- test data pipelines locally\n- worry less about building infrastructure\n\n**Teal is alpha quality - unstable, but usable.**\n\n[Play with Teal in your browser!](https://www.condense9.com/playground)\n\n```shell\n$ pip install teal-lang\n```\n\nGetting started:\n- Clone this repository\n- `poetry install`\n- See [the hello example](examples/hello) to get started\n\n*Do not be afraid, the parentheses will not harm you.*\n\n---\n\n\n### Known Limitations and Issues\n\nOnly one program file is supported (module/package system coming soon).\n\nThere\'s no error handling. Coming soon!\n\nThe tests are pretty much all broken.\n',
    'author': 'Ric da Silva',
    'author_email': 'ric@condense9.com',
    'maintainer': 'Ric da Silva',
    'maintainer_email': 'ric@condense9.com',
    'url': 'https://www.condense9.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
