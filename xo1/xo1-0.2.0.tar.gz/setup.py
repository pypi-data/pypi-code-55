# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xo1']

package_data = \
{'': ['*']}

install_requires = \
['eaf>=0.2,<0.3']

setup_kwargs = {
    'name': 'xo1',
    'version': '0.2.0',
    'description': 'EAF-based framework for creating terminal applications',
    'long_description': '|PyPI| |Build Status| |codecov.io|\n\n===\nxo1\n===\n\nPython framework for creating terminal applications.\n\nRequirements\n============\n\n* >=python-3.7\n* >=eaf-0.2\n\nInstallation\n============\n\n.. code-block:: console\n\n\t$ pip install xo1\n\n\nDevelopment\n===========\n\nInstallation\n------------\n\n.. code-block:: console\n\n   $ poetry install\n\nTesting\n-------\n\n.. code-block:: console\n\n   $ poetry run pytest -s -v tests/  # run all tests\n   $ poetry run pytest --cov=xo1 -s -v tests/  # run all tests with coverage\n   $ poetry run black xo1/ tests/  # autoformat code\n   $ # run type checking\n   $ poetry run pytest --mypy --mypy-ignore-missing-imports -s -v xo1/ tests/\n   $ # run code linting\n   $ poetry run pytest --pylint -s -v xo1/ tests/\n\nDocumentation\n-------------\n\n* **To be added**\n\n.. |PyPI| image:: https://badge.fury.io/py/xo1.svg\n   :target: https://badge.fury.io/py/xo1\n.. |Build Status| image:: https://github.com/pkulev/xo1/workflows/CI/badge.svg\n.. |codecov.io| image:: http://codecov.io/github/pkulev/xo1/coverage.svg?branch=master\n   :target: http://codecov.io/github/pkulev/xo1?branch=master\n',
    'author': 'Pavel Kulyov',
    'author_email': 'kulyov.pavel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pkulev/xo1',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
