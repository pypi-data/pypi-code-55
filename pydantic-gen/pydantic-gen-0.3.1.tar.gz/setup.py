# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_gen']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'black>=19.10b0,<20.0',
 'jinja2>=2.11.2,<3.0.0',
 'pydantic>=1.4,<2.0',
 'python-box>=4.2.2,<5.0.0',
 'ruamel.yaml>=0.16.10,<0.17.0']

setup_kwargs = {
    'name': 'pydantic-gen',
    'version': '0.3.1',
    'description': 'Code generator for pydantic schemas',
    'long_description': "# Pydantic Schemas Generator\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydantic-gen)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/pydantic-gen)](https://pypi.org/project/pydantic-gen/)\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Flicht1stein%2Fpydantic-gen%2Fbadge&style=flat)](https://actions-badge.atrox.dev/licht1stein/pydantic-gen/goto)\n\n\n## What this package does\nThis is a code generation package that converts YML definitions to Pydantic models (either python code or python objects).\n\n\n## What is Pydantic \n[Pydantic](https://pydantic-docs.helpmanual.io/) is a python library for data validation and settings management using \npython type annotations.\n\nHere's an [official example](https://pydantic-docs.helpmanual.io/#example) from the docs\n\n## Why generate schemas?\n\nNormally you just program the schemas within your program, but there are several \nuse cases when code generation makes a lot of sense:\n\n* You're programming several apps that use the same schema (think an API server \nand client library for it)\n* You're programming in more than one programming language\n\n## Getting started\n\n### Installation\n\n`pip install pydantic-gen`\n\n\n### Usage\n\nFirst you need to create a YAML file with your desired class schema. See \n[example.yml](./example.yml) file.\n\n```python\nfrom pydantic_gen import SchemaGen\n\ngenerated = SchemaGen('example.yml')\n```\n\nThe code is now generated and stored in `generated.code` attribute. There are \ntwo ways to use the code:\n\n**1. Save it to a file, and use the file in your program.**\n\n```python\ngenerated.to_file('example_output.py')\n```\n\nYou can inspect the resulting [example_output.py](./example_output.py)\n\n**2. Import the generated classed directly without saving**\n\n```python\ngenerated.to_sys(module_name='generated_schemas')\n```\n\nAfter running `.to_sys()` module `'generated_schemas'` will be added to\n`sys.modules` and become importable like a normal module:\n\n```python\nfrom generated_schemas import GeneratedSchema1\n\nschema = GeneratedSchema1(id=1)\n``` \n\n### Usage pattern\n\nRecommended usage pattern is creating the yaml files needed for your projects\nand storing them in a separate repository, to achieve maximum consistency across all projects.\n\n### YAML-file structure\n\n`schemas` - list of all schemas described\n\n`name` - name of the generated class\n\n`props` - list of properties of the class using python type \nannotation. Fields: `name` - field name, `type` - field type,\n`optional` - bool, if True the type will be wrapped in `Optional`,\n`default` - default value for the field.\n\n`config` - list of config settings from [Model Config](https://pydantic-docs.helpmanual.io/usage/model_config/)\nof pydantic.\n\n### Testing\n\nProject is fully covered by tests.\n\n### Packaging notice\nThis project uses the excellent [poetry](https://python-poetry.org) for packaging. Please read about it and let's all start using\n`pyproject.toml` files as a standard. Read more:\n\n* [PEP 518 -- Specifying Minimum Build System Requirements for Python Projects](https://www.python.org/dev/peps/pep-0518/)\n\n* [What the heck is pyproject.toml?](https://snarky.ca/what-the-heck-is-pyproject-toml/)\n\n* [Clarifying PEP 518 (a.k.a. pyproject.toml)](https://snarky.ca/clarifying-pep-518/)\n\n\n",
    'author': 'MB',
    'author_email': 'mb@blaster.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/licht1stein/pydantic-gen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
