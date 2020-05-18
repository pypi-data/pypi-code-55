# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pep440_version_utils']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=20.3,<21.0']

setup_kwargs = {
    'name': 'pep440-version-utils',
    'version': '0.3.0',
    'description': 'Utilities to deal with pep440 versioning',
    'long_description': '![Continuous Integration](https://github.com/m-vdb/pep440-version-utils/workflows/Continuous%20Integration/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/m-vdb/pep440-version-utils/badge.svg?branch=master)](https://coveralls.io/github/m-vdb/pep440-version-utils?branch=master)\n\n# pep440-version-utils\nThis package regroups utilities to deal with pep440 versioning. It is based on the\n[PyPA\'s `packaging`](https://github.com/pypa/packaging) project and extends it.\n\nIt makes it easier to handle version bumps and strictly follows [PEP440 specification](https://www.python.org/dev/peps/pep-0440/).\n\n![Release cycle](https://github.com/m-vdb/pep440-version-utils/blob/master/docs/release-cycle.png?raw=true)\n\n## Installation\n\nUse `pip` or `poetry` to install this package:\n\n```bash\n$ pip install pep440-version-utils\n\n# or alternatively\n$ poetry add pep440-version-utils\n```\n\n## Usage\n\nSince this package extends the `packaging` library, so it supports version parsing and ordering as described\nin [this documentation](https://packaging.pypa.io/en/latest/version/).\n\nTo bump to a new release version:\n\n```python\nfrom pep440_version_utils import Version\n\nversion = Version("1.10.2")\nversion.next_micro()  # 1.10.3\nversion.next_minor()  # 1.11.0\nversion.next_major()  # 2.0.0\n```\n\nTo bump to a new prerelease version:\n\n```python\nfrom pep440_version_utils import Version\n\nversion = Version("1.10.2")\nversion.next_alpha()  # 1.10.3a1\nversion.next_beta()  # 1.10.3b1\nversion.next_release_candidate()  # 1.10.3rc1\n\nversion.next_alpha("minor")  # 1.11.0a1\nversion.next_beta("mior")  # 1.11.0b1\nversion.next_release_candidate("major")  # 2.0.0rc1\n```\n\nAnd it implements the full release cycle:\n\n```python\nfrom pep440_version_utils import Version\n\nversion = Version("1.10.2")\nalpha1 = version.next_alpha()  # 1.10.3a1\nalpha2 = alpha1.next_alpha()  # 1.10.3a2\nbeta1 = alpha2.next_beta()  # 1.10.3b1\nrc1 = beta1.next_release_candidate()  # 1.10.3rc1\nrc2 = rc1.next_release_candidate()  # 1.10.3rc2\nnew_version = rc2.next_micro()  # 1.10.3\n```\n\nYou can also check if a version is a specific type of prerelease:\n```python\nfrom pep440_version_utils import Version\n\nVersion("1.10.2a1").is_alpha  # True\nVersion("1.10.2b2").is_beta  # True\nVersion("1.10.2rc1").is_release_candidate  # True\n```\n\n## Limitations\n\nThis package doesn\'t support _post_, _dev_ and _local_ versions yet. **Contributions are welcome 😊**\n\n## How to contribute\n\nThis package is fairly simple, here is how you can contribute:\n\n1. ⚙️ Install [`poetry`](https://python-poetry.org/)\n2. 📦 In the repository folder, run `poetry install`\n3. ✍️ Implement the desired changes\n4. ✅ Run test, type checking and code quality checks:\n```bash\n$ poetry run black . --check\n$ poetry run mypy */**.py --ignore-missing-imports\n$ poetry run pytest --cov=pep440_version_utils\n```\n5. ➡️ Submit a new pull request\n\nDo not hesitate to contribue, even for very small changes!\n',
    'author': 'Maxime Verger',
    'author_email': 'me@maxvdb.com',
    'maintainer': 'Maxime Verger',
    'maintainer_email': 'me@maxvdb.com',
    'url': 'https://github.com/m-vdb/pep440-version-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
