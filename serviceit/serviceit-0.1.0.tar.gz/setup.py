# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serviceit']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.6,<2.0', 'tomlkit>=0.6.0,<0.7.0', 'typer>=0.2,<0.3']

setup_kwargs = {
    'name': 'serviceit',
    'version': '0.1.0',
    'description': 'Turn any Python function into a service that receives JSON payloads on some port.',
    'long_description': "# Service-it\n\n[![Version status](https://img.shields.io/pypi/status/serviceit)](https://pypi.org/project/serviceit/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/serviceit)](https://pypi.org/project/serviceit/)\n[![Docker](https://img.shields.io/docker/v/dmyersturnbull/serviceit?color=green&label=DockerHub)](https://hub.docker.com/repository/docker/dmyersturnbull/serviceit)\n[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/service-it?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/service-it/releases)\n[![Latest version on PyPi](https://badge.fury.io/py/serviceit.svg)](https://pypi.org/project/serviceit/)\n[![Documentation status](https://readthedocs.org/projects/service-it/badge/?version=latest&style=flat-square)](https://service-it.readthedocs.io/en/stable/)\n[![Build & test](https://github.com/dmyersturnbull/service-it/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/service-it/actions)\n[![Maintainability](https://api.codeclimate.com/v1/badges/cb9bc2733ece01a8800b/maintainability)](https://codeclimate.com/github/dmyersturnbull/service-it/maintainability)\n[![Coverage](https://coveralls.io/repos/github/dmyersturnbull/service-it/badge.svg?branch=master)](https://coveralls.io/github/dmyersturnbull/service-it?branch=master)\n\nTurn any Python function into a service that receives JSON payloads on some port.\n\nHere's a trivial example:\n\n```python\nimport serviceit\ndef receiver(payload):\n    print(payload)\nserver = serviceit.server(1533, receiver)\n# Now it will receive JSON on 1533. For convenience:\nserver.client().send(dict(message='hi'))\nprint(server.bytes_processed)\n```\n\n#### More complex example: isolate code\nYou can use this to isolate a component of you code.\nFor example, rdkit can be installed through Conda but not Pip (or Poetry).\nSo, create a service and import it in an Anaconda environment to create a server,\nand in your pip-installed client code.\n\n**In a Conda environment**, create a service that listens on port 1533:\n\n```python\nimport serviceit\n\ndef _receiver(payload):\n    # noinspection PyUnresolvedReferences\n    from rdkit.Chem.inchi import InchiToInchiKey\n    inchikey = InchiToInchiKey(payload['inchi'])\n    print(inchikey)\n\nserver = serviceit.server(1533, _receiver)\n```\n\n**On your pip-install client side:**\n\n```python\nimport serviceit\nclient = serviceit.client(1533)\nclient.send(dict(inchi='InChI=1S/H2O/h1H2'))\n```\n\n\n[New issues](https://github.com/dmyersturnbull/service-it/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/service-it/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n",
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/service-it',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
