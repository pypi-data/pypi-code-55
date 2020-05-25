# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opcsim', 'opcsim.equations']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'opcsim',
    'version': '0.5.0rc6',
    'description': 'OPCSIM: simulating low-cost optical particle counters',
    'long_description': '[![PyPI version](https://badge.fury.io/py/opcsim.svg)](https://badge.fury.io/py/opcsim)\n[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/dhhagan/opcsim/blob/master/LICENSE)\n![build and test](https://github.com/dhhagan/opcsim/workflows/Run%20unittests%20and%20push%20to%20coveralls/badge.svg)\n[![codecov](https://codecov.io/gh/dhhagan/opcsim/branch/master/graph/badge.svg)](https://codecov.io/gh/dhhagan/opcsim)\n![Docker Pulls](https://img.shields.io/docker/pulls/dhhagan/opcsim)\n![Docker Stars](https://img.shields.io/docker/stars/dhhagan/opcsim)\n\n# opcsim\n\nopcsim is a Python library for simulating low-cost Optical Particle Sensors (both Optical Particle Counters and Nephelometers) and\ntheir response to various aerosol distributions.\n\n## Documentation\n\nFull online documentation can be found [here][1].\n\nThe docs include a [tutorial][2], an [example gallery][3], and an [API Reference][4].\n\nIn addition, documentation can be built locally for development purposes. To do so, please check out the complete details in the *contributing to opcsim* section of the documentation.\n\n## Docker\n\nIf you are familiar with Docker, there is a Docker image available to get up and running with OPCSIM with ease. To get started \nwith an ephemeral container with a jupyter lab interface, navigate to your preferred working directory and execute:\n\n```sh\n$ docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/joyvan/work dhhagan/opcsim:latest\n```\n\nOnce executed, you should see the url with token in your terminal that will allow you to bring up the jupyter lab instance.\n\n\n## Dependencies\n\nOpcsim is supported for python3.6.1+.\n\nInstallation requires [scipy][5], [numpy][6], [pandas][7], [matplotlib][8],\nand [seaborn][9].\n\n\n## Installation\n\nTo install (or upgrade to) the latest stable release:\n\n```sh\n\n$ pip install opcsim [--upgrade]\n```\n\nTo install the development version directly from GitHub using pip:\n\n```sh\n\n$ pip install git+https://github.com/dhhagan/opcsim.git\n```\n\nIn addition, you can either clone the repository and install from source or download/unzip the zip file and install from source using poetry:\n\n```sh\n\n$ git clone https://github.com/dhhagan/opcsim.git\n$ cd /opcsim\n$ poetry install\n```\n\n## Testing\n\nAll tests are automagically run via GitHub actions and Travis.ci. For results of these tests, please click on the link in the above travis badge. In addition, you can run tests locally using poetry.\n\nTo run tests locally:\n\n```sh\n\n$ poetry run pytest tests\n```\n\n\n## Development\n\n**opcsim** development takes place on GitHub. Issues and bugs can be submitted and tracked via the [GitHub Issue Tracker][10] for this repository. As of `v0.5.0`, *opcsim* uses [poetry][11] for versioning and managing dependencies and releases.\n\n\n[1]: https://dhhagan.github.io/opcsim/\n[2]: https://dhhagan.github.io/opcsim/tutorial.html\n[3]: https://dhhagan.github.io/opcsim/examples/index.html\n[4]: https://dhhagan.github.io/opcsim/api.html\n[5]: https://www.scipy.org/\n[6]: http://www.numpy.org/\n[7]: http://pandas.pydata.org/\n[8]: http://matplotlib.org/\n[9]: https://seaborn.pydata.org/\n[10]: https://github.com/dhhagan/opcsim/issues\n[11]: https://python-poetry.org/\n',
    'author': 'David H Hagan',
    'author_email': 'dhagan@mit.edu',
    'maintainer': 'David H Hagan',
    'maintainer_email': 'dhagan@mit.edu',
    'url': 'https://dhhagan.github.io/opcsim/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
