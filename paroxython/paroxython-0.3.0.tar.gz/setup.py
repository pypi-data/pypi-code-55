# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paroxython', 'paroxython.cli']

package_data = \
{'': ['*'], 'paroxython': ['resources/*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'regex>=2020.5.14,<2021.0.0',
 'sqlparse>=0.3.1,<0.4.0',
 'typed-ast>=1.4.1,<2.0.0',
 'typing-extensions>=3.7.4.2,<4.0.0.0']

entry_points = \
{'console_scripts': ['paroxython = paroxython.cli.cli:main']}

setup_kwargs = {
    'name': 'paroxython',
    'version': '0.3.0',
    'description': 'Search Python code for algorithmic features',
    'long_description': '[![Build Status](https://travis-ci.com/laowantong/paroxython.svg?branch=master)](https://travis-ci.com/laowantong/paroxython)\n[![codecov](https://img.shields.io/codecov/c/github/laowantong/paroxython/master)](https://codecov.io/gh/laowantong/paroxython)\n[![Checked with mypy](https://img.shields.io/badge/typing-mypy-brightgreen)](http://mypy-lang.org/)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/73432ed4c5294326ba6279bbbb0fe2e6)](https://www.codacy.com/manual/laowantong/paroxython)\n[![Updates](https://pyup.io/repos/github/laowantong/paroxython/shield.svg)](https://pyup.io/repos/github/laowantong/paroxython/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/paroxython)\n[![GitHub Release](https://img.shields.io/github/release/laowantong/paroxython.svg?style=flat)]()\n![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/laowantong/paroxython)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/laowantong/paroxython.svg?style=flat)]()\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n![](docs/resources/logo.png)\n\nParoxython is a command-line tool which finds and tags algorithmic features (such as assignments, nested loops, tail-recursive functions, etc.) in a collection of small Python programs, typically gathered for educational purposes (e.g., examples, patterns, exercise corrections).\n\nEach tag consists in a free-form label associated with its spanning lines. These labels are then mapped onto a knowledge taxonomy designed by the teacher with basic order constraints in mind (e.g., the fact that the introduction of the concept of early exit must come after that of loop, which itself requires that of control flow, is expressed with the following taxon: flow/loop/exit/early).\n\nSource codes, labels and taxons are stored in a database, which can finally be filtered through a pipeline of inclusion, exclusion and impartment commands on programs or taxons.\n\n# Installation\n\n```\npip install paroxython\n```\n\n# Test-drive\n\n## Terminal\n```\nparoxython --help\n```\n\n## Jupyter notebook\n\nLoad the magic command:\n\n```python\n%load_ext paroxython\n```\n\nRun it on a cell of Python code (line numbers added for clarity):\n\n```python\n1\t%%paroxython\n2\tdef fibonacci(n):\n3\t    result = []\n4\t    (a, b) = (0, 1)\n5\t    while a < n:\n6\t        result.append(a)\n7\t        (a, b) = (b, a + b)\n8\t    return result\n```\n\n\n| Taxon | Lines |\n|:--|--:|\n| `call/method/append` | 6 |\n| `flow/loop/exit/late` | 5-7 |\n| `flow/loop/while` | 5-7 |\n| `metadata/sloc/8` | 2-8 |\n| `operator/arithmetic/addition` | 7 |\n| `subroutine/argument/arg` | 2 |\n| `subroutine/function` | 2-8 |\n| `test/inequality` | 5 |\n| `type/number/integer/literal` | 4 |\n| `type/number/integer/literal/zero` | 4 |\n| `type/sequence/list` | 6 |\n| `type/sequence/list/literal/empty` | 3 |\n| `type/sequence/tuple/literal` | 4, 4, 7, 7 |\n| `variable/assignment/parallel` | 4 |\n| `variable/assignment/parallel/slide` | 7 |\n| `variable/assignment/single` | 3 |\n\n# Documentation\n\nComing soon.\n',
    'author': 'Aristide Grange',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/laowantong/paroxython/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
