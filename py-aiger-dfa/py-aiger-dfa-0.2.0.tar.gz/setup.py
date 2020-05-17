# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_dfa']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'bidict>=0.18.0,<0.19.0',
 'dfa>=0.3.2,<0.4.0',
 'funcy>=1.12,<2.0',
 'py-aiger-bv>=4.0.0,<5.0.0',
 'py-aiger-ptltl>=3.0.0,<4.0.0',
 'py-aiger>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'py-aiger-dfa',
    'version': '0.2.0',
    'description': 'Library for moving between sequential circuits AIGs and DFAs.',
    'long_description': "# py-aiger-dfa\nPython library for converting between AIG circuits and DFAs.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-dfa/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-dfa)\n[![Docs](https://img.shields.io/badge/API-link-color)](https://mvcisback.github.io/py-aiger-dfa)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-dfa/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-dfa)\n[![PyPI version](https://badge.fury.io/py/py-aiger-dfa.svg)](https://badge.fury.io/py/py-aiger-dfa)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n    - [DFA to AIG](#dfa-to-aig)\n    - [AIG to DFA](#aig-to-dfa)\n\n<!-- markdown-toc end -->\n\n\n# Installation\n\nIf you just need to use `aiger_dfa`, you can just run:\n\n`$ pip install py-aiger-dfa`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\nThe main entry points for using this library are the `dfa2aig` and\n`aig2dfa` functions. DFAs are represented using the\n[dfa](https://github.com/mvcisback/dfa) package. Familiarity with the\n`dfa`, `py-aiger`, and `py-aiger-bv` packages is assumed.\n\n\n## DFA to AIG\n\nAn example of going from a `DFA` to an `AIG` object\nis shown below.\n\n```python\nfrom dfa import DFA\nfrom aiger_dfa import dfa2aig\n\nmy_dfa = DFA(\n    start=0,\n    inputs={0, 1},\n    label=lambda s: (s % 4) == 3,\n    transition=lambda s, c: (s + c) % 4,\n)\nmy_aig, relabels, valid = dfa2aig(my_dfa)\n```\n\nNow `circ` is an `AIG` and `relabels` is a mapping from the inputs,\nstates, and outputs of `my_dfa` to their **1-hot** encoded\ncounterparts in `my_aig`.\n\n`relabels` has the following schema:\n\n```python\nrelabels = {\n    'inputs': .. , # Bidict from 1-hot encoded tuple to dfa input.\n    'outputs': .. , # Bidict from 1-hot encoded tuple to dfa output.\n    'states': .. , # Bidict from 1-hot encoded tuple to dfa state.\n}\n```\n\nwhere `bidict` refers to https://bidict.readthedocs.io/en/master/.\nFinally, `valid` is another aiger circuit which tests if all inputs\nare 1-hot encoded.\n\n## AIG to DFA\n\nThe inverse of `dfa2aig` is `aig2dfa`. Using the same example.\n\n```python\nfrom aiger_dfa import aig2dfa\n\nmy_dfa2 = aig2dfa(my_aig, relabels=relabels)\n\nassert my_dfa2.label((1,0,0,1,1,0)) == my_dfa.label((1,0,0,1,1,0))\n```\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-dfa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
