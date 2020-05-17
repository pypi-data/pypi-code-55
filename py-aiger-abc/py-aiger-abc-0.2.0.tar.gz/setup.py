# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_abc']

package_data = \
{'': ['*']}

install_requires = \
['py-aiger>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'py-aiger-abc',
    'version': '0.2.0',
    'description': 'Bridge to using Berkeley-ABC with py-aiger.',
    'long_description': "# py-aiger-abc\nAiger <-> ABC bridge\n\n[![PyPI version](https://badge.fury.io/py/py-aiger-abc.svg)](https://badge.fury.io/py/py-aiger-abc)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n# Installation\n\n## Non-Python Dependencies\n\nThis package currently assumes that the\n[ABC](https://github.com/berkeley-abc/abc) and\n[aigtoaig](http://fmv.jku.at/aiger/) commands are installed and in the\nPATH. In the future, we hope to automatically include these\ndependencies, but currently one needs to install them on their own.\n\n## Python Package\n\nIf you just need to use `aiger_abc`, you can just run:\n\n`$ pip install py-aiger-abc`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then run:\n\n`$ poetry install`\n\n# Usage\n\nThe primary entry point for using `aiger_abc` is the `simplify`\nfunction which uses `abc` to simplify an AIG. For example, below we\nshow how `aiger_abc` can be used to simplify the following inefficient\nencoding of const false.\n\n```python\nimport aiger\n\nx = aiger.atom('x')\n\nf = x ^ x\nprint(f.aig)\n```\n\n```\naag 4 1 0 1 3\n2\n8\n4 2 2\n6 3 3\n8 5 7\n```\n\n```python\nimport aiger_abc\nf2 = aiger_abc.simplify(f)\nprint(f2.aig)\n```\n\n```\naag 1 1 0 1 0\n2\n0\n```\n\n## Explicitly Specifying for `abc` and `aigtoaig` commands\n\n`simplify` supports explicitly specifying the\n`abc` and `aigtoaig` commands. This is useful\nif you have installed them in non-standard paths\nor names. E.g.,\n\n```python\nf2 = aiger_abc.simplify(f, abc_cmd='abc', aigtoaig_cmf='aigtoaig')\n```\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-abc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
