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
    'version': '0.3.3',
    'description': 'Code generator for pydantic schemas',
    'long_description': "==========================\nPydantic Schemas Generator\n==========================\n.. image:: https://img.shields.io/pypi/pyversions/pydantic-gen\n    :target: https://pypi.org/project/pydantic-gen/\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n.. image:: https://img.shields.io/pypi/v/pydantic-gen\n    :target: https://pypi.org/project/pydantic-gen/\n.. image:: https://img.shields.io/pypi/dw/pydantic-gen\n    :target: https://pypi.org/project/pydantic-gen/\n.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Flicht1stein%2Fpydantic-gen%2Fbadge&style=flat\n    :target: https://actions-badge.atrox.dev/licht1stein/pydantic-gen/goto\n.. image:: https://img.shields.io/readthedocs/pydantic-gen   :alt: Read the Docs\n    :target: https://pydantic-gen.readthedocs.io/en/latest/\n.. image:: https://img.shields.io/badge/Support-With_coffee!-Green\n    :target: https://www.buymeacoffee.com/licht1stein\n\n----------------------\nWhat this package does\n----------------------\nThis is a code generation package that converts YML definitions to Pydantic models (either python code or python objects).\n\n----------------\nWhat is Pydantic\n----------------\n`Pydantic <https://pydantic-docs.helpmanual.io/>`_ is a python library for data validation and settings management using\npython type annotations.\n\nTake a look at the `official example <https://pydantic-docs.helpmanual.io/#example>`_ from the Pydantic docs.\n\n---------------------\nWhy generate schemas?\n---------------------\nNormally you just program the schemas within your program, but there are several\nuse cases when code generation makes a lot of sense:\n\n- You're programming several apps that use the same schema (think an API server and client library for it)\n\n- You're programming in more than one programming language\n\n---------------\nGetting started\n---------------\n\nInstallation\n------------\nUsing pip:\n\n.. code-block:: bash\n\n    pip install pydantic-gen\n\nUsing `poetry <https://python-poetry.org/>`_:\n\n.. code-block:: bash\n\n    poetry add pydantic-gen\n\nUsage\n-----\nFirst you need to create a YAML file with your desired class schema. See `example.yml <https://github.com/licht1stein/pydantic-gen/blob/documentation/example.yml>`_ file.\n\n.. code-block:: python\n\n    from pydantic_gen import SchemaGen\n\n    generated = SchemaGen('example.yml')\n\nThe code is now generated and stored in `generated.code` attribute. There are\ntwo ways to use the code:\n\n1. Save it to a file, and use the file in your program:\n\n.. code-block:: python\n\n    generated.to_file('example_output.py')\n\nYou can inspect the resulting file in the `example_output.py <https://github.com/licht1stein/pydantic-gen/blob/documentation/example_output.py>`_\n\n2. Or directly import the generated classed directly without saving:\n\n.. code-block:: python\n\n    generated.to_sys(module_name='generated_schemas')\n\nAfter running `generated.to_sys(module_name='generated_schemas'` your generated code will be available for import:\n\n.. code-block:: python\n\n    import generated_schemas as gs\n\n    schema = gs.GeneratedSchema1(id=1)\n\nUsage pattern\n-------------\nRecommended usage pattern is creating the yaml files needed for your projects\nand storing them in a separate repository, to achieve maximum consistency across all projects.\n\nYAML-file structure\n-------------------\n`schemas` - list of all schemas described\n\n`name` - name of the generated class\n\n`props` - list of properties of the class using python type\nannotation. Fields: `name` - field name, `type` - field type,\n`optional` - bool, if True the type will be wrapped in `Optional`,\n`default` - default value for the field.\n\n`config` - list of config settings from `Model Config <https://pydantic-docs.helpmanual.io/usage/model_config/>`_\nof pydantic.\n\nTesting\n-------\nProject is fully covered by tests and uses pytest. To run:\n\n.. code-block:: bash\n\n    pytest\n\nPackaging Notice\n----------------\nThis project uses the excellent `poetry <https://python-poetry.org>`__ for packaging. Please read about it and let's all start using\n`pyproject.toml` files as a standard. Read more:\n\n* `PEP 518 -- Specifying Minimum Build System Requirements for Python Projects <https://www.python.org/dev/peps/pep-0518/>`_\n\n* `What the heck is pyproject.toml? <https://snarky.ca/what-the-heck-is-pyproject-toml/>`_\n\n* `Clarifying PEP 518 (a.k.a. pyproject.toml) <https://snarky.ca/clarifying-pep-518/>`_\n\n\n\n",
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
