# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nox_poetry']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['nox-poetry = nox_poetry.__main__:main']}

setup_kwargs = {
    'name': 'nox-poetry',
    'version': '0.1.0',
    'description': 'nox-poetry',
    'long_description': "\nnox-poetry\n==========\n\n|Tests| |Codecov| |PyPI| |Python Version| |Read the Docs| |License| |Black| |pre-commit| |Dependabot|\n\n.. |Tests| image:: https://github.com/cjolowicz/nox-poetry/workflows/Tests/badge.svg\n   :target: https://github.com/cjolowicz/nox-poetry/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/cjolowicz/nox-poetry/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/cjolowicz/nox-poetry\n   :alt: Codecov\n.. |PyPI| image:: https://img.shields.io/pypi/v/nox-poetry.svg\n   :target: https://pypi.org/project/nox-poetry/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/nox-poetry\n   :target: https://pypi.org/project/nox-poetry\n   :alt: Python Version\n.. |Read the Docs| image:: https://readthedocs.org/projects/nox-poetry/badge/\n   :target: https://nox-poetry.readthedocs.io/\n   :alt: Read the Docs\n.. |License| image:: https://img.shields.io/pypi/l/nox-poetry\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=cjolowicz/nox-poetry\n   :target: https://dependabot.com\n   :alt: Dependabot\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *nox-poetry* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install nox-poetry\n\n\nUsage\n-----\n\n* TODO\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*nox-poetry* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/cjolowicz/nox-poetry/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n",
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/nox-poetry',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
