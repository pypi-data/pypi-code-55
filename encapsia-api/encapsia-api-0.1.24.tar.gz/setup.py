# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['encapsia_api', 'encapsia_api.tests']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.13.1,<0.14.0',
 'requests[security]>=2.20,<3.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'encapsia-api',
    'version': '0.1.24',
    'description': 'Client API for talking to an Encapsia system.',
    'long_description': '# Encapsia API Library\n\n![Tests](https://github.com/tcorbettclark/encapsia-api/workflows/Tests/badge.svg)\n\n[![Known Vulnerabilities](https://snyk.io/test/github/tcorbettclark/encapsia-api/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/tcorbettclark/encapsia-api?targetFile=requirements.txt)\n\nREST API for working with Encapsia.\n\nSee <https://www.encapsia.com.>\n\n## Release checklist\n\n* Run: `black .`\n* Run: `isort`\n* Run: `flake8 .`\n* Run: `nose2 -v`\n* Run: `poetry export -f requirements.txt >requirements.txt` (for snyk scanning)\n* Ensure `git tag`, package version (via `poetry version`), and `encapsia_api.__version__` are all equal.',
    'author': 'Timothy Corbett-Clark',
    'author_email': 'timothy.corbettclark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tcorbettclark/encapsia-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
