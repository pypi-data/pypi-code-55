# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antsibull',
 'antsibull.changelog',
 'antsibull.cli',
 'antsibull.data',
 'antsibull.schemas',
 'tests',
 'tests.functional.changelog',
 'tests.functional.changelog-yaml',
 'tests.functional.schema',
 'tests.units']

package_data = \
{'': ['*'],
 'tests.functional.changelog-yaml': ['bad/*', 'good/*'],
 'tests.functional.schema': ['good_data/*']}

install_requires = \
['PyYAML',
 'aiofiles',
 'aiohttp',
 'docutils',
 'jinja2',
 'packaging',
 'pydantic',
 'rstcheck>=3,<4',
 'semantic_version',
 'sh']

entry_points = \
{'console_scripts': ['antsibull-build = antsibull.cli.antsibull_build:main',
                     'antsibull-changelog = '
                     'antsibull.cli.antsibull_changelog:main',
                     'antsibull-lint-changelog-yaml = '
                     'antsibull.cli.antsibull_lint_changelog_yaml:main']}

setup_kwargs = {
    'name': 'antsibull',
    'version': '0.1.0',
    'description': 'Tools for building the Ansible Distribution',
    'long_description': "# antsibull -- Ansible Build Scripts\nTooling for building various things related to Ansible\n\nScripts that are here:\n\n* antsibull-build - Builds Ansible-2.10+ from component collections ([docs](docs/build-ansible.rst))\n* antsibull-docs - Extracts documentation from ansible plugins\n* antsibull-changelog - Changelog generator for Ansible collections and ansible-base ([docs](docs/changelogs.rst))\n* antsibull-lint-changelog-yaml - Validates ``changelogs/changelog.yaml`` files ([docs](docs/changelog.yaml-format.md))\n\nScripts are created by poetry at build time.  So if you want to run from\na checkout, you'll have to run them under poetry::\n\n    python3 -m pip install poetry\n    poetry install  # Installs dependencies into a virtualenv\n    poetry run antsibull-build --help\n\nIf you want to create a new release::\n\n    poetry build\n    poetry publish  # Uploads to pypi.  Be sure you really want to do this\n\n.. note:: When installing a package published by poetry, it is best to use\n    pip >= 19.0.  Installing with pip-18.1 and below could create scripts which\n    use pkg_resources which can slow down startup time (in some environments by\n    quite a large amount).\n\nUnless otherwise noted in the code, it is licensed under the terms of the GNU\nGeneral Public License v3 or, at your option, later.\n",
    'author': 'Toshio Kuratomi',
    'author_email': 'a.badger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ansible-community/antsibull',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
