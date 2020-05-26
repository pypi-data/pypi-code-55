# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssrm_test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0',
 'scipy>=1.3,<2.0',
 'toolz>=0.10.0,<0.11.0',
 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'ssrm-test',
    'version': '0.1.3',
    'description': 'A library for Sequential Sample Ratio Mismatch (SRM) test.',
    'long_description': '![Build](https://github.com/optimizely/ssrm/workflows/Build/badge.svg)\n\n# <img src="logos/ssrm-blue.png" alt="ssrm-logo" width="40"/> SSRM: A Sequential Sample Ratio Mismatch Test\nA package for sequential testing of Sample Ratio Mismatch (SRM).\n\nContributors:\n- Michael Lindon (michael.lindon@optimizely.com )\n\n## Installation\nWe recommend that you use an isolated virtual environment to install and run the code in this repo (See: [virtualenv](https://pypi.org/project/virtualenv/) and [pyenv](https://github.com/pyenv/pyenv))\n\n1. You can clone the repository from the command-line:\n    ```console\n    git clone git@github.com:optimizely/ssrm.git\n    ```\n    We highly recommend that you branch off of `master` and pull in upstream changes regularly.\n1. Install dependencies: Run `make install`.\n    - If you wish to develop in the repo, run `make install-dev`.  Also, see the contributing doc [here](https://github.com/optimizely/ssrm/blob/master/CONTRIBUTING.md)\n    > **Tip:** have a look in the [Makefile](https://github.com/optimizely/ssrm/blob/master/Makefile) to learn more about what this, and other make recipes do!\n1. Run tests:\n    -   `make check` to run all checks.\n    -   `make test` to run unit tests.\n\n\n## Tutorials\nWe provide a tutorial notebook that walks through an example of running a\nSequential SRM test\n[here](https://github.com/optimizely/ssrm/blob/master/notebooks/introduction.ipynb).  Run `jupyter lab`, and open `notebooks/introduction.ipynb`.\n\n## Documentation\nThe latest reference documentation is here (TBD).\n\n## Contributing\nSee the contributing doc [here](https://github.com/optimizely/ssrm/blob/master/CONTRIBUTING.md).\n\n### Credits\nFirst-party code (under `ssrm_test`) is copyright Optimizely, Inc. and contributors, licensed under Apache 2.0.\n\n### Additional Code\nThis software incorporates code from the following open source projects:\n\n**numpy** [https://numpy.org/index.html](https://numpy.org/index.html)\n- Copyright © 2005-2020, NumPy Developers.\n- License (BSD): https://numpy.org/license.html#license\n\n**scipy** [https://www.scipy.org/scipylib/index.html](https://www.scipy.org/scipylib/index.html)\n- Copyright © 2001-2002 Enthought, Inc.  2003-2019, SciPy Developers.\n- License (BSD): https://www.scipy.org/scipylib/license.html\n\n**toolz** [https://github.com/pytoolz/toolz](https://github.com/pytoolz/toolz)\n- Copyright © 2013 Matthew Rocklin\n- License (New BSD): https://github.com/pytoolz/toolz/blob/master/LICENSE.txt\n\n**typing** [https://github.com/python/typing](https://github.com/python/typing)\n- Copyright © 2001-2014 Python Software Foundation; All Rights Reserved.\n- License (Python Software Foundation License (PSF)): https://github.com/python/typing/blob/master/LICENSE\n',
    'author': 'Michael Lindon',
    'author_email': 'michael.lindon@optimizely.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/optimizely/ssrm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
