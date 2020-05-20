# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numiner', 'numiner.classes']

package_data = \
{'': ['*']}

install_requires = \
['coveralls>=2.0.0,<3.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'pandas>=1.0.3,<2.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['numiner = numiner.__main__:main',
                     'version = numiner.__main__:get_version']}

setup_kwargs = {
    'name': 'numiner',
    'version': '0.2.1',
    'description': 'NUM Miner (Tool to create open dataset for Handwritten Text Recognition)',
    'long_description': '<h1 align="center">\n  NUMiner\n</h1>\n\n<p align="center">\n  <a href="https://travis-ci.org/khasbilegt/numiner">\n    <img src="https://travis-ci.org/khasbilegt/numiner.svg?branch=master" alt="Build Status">\n  </a>\n  <a href="https://github.com/PyCQA/bandit">\n    <img src="https://img.shields.io/badge/security-bandit-yellow.svg"\n         alt="security: bandit">\n  </a>\n  <a href="https://badge.fury.io/py/numiner">\n    <img src="https://badge.fury.io/py/numiner.svg" alt="PyPI version">\n  </a>\n  <a href=\'https://coveralls.io/github/khasbilegt/numiner?branch=master\'>\n    <img src=\'https://coveralls.io/repos/github/khasbilegt/numiner/badge.svg?branch=master\' alt=\'Coverage Status\' />\n  </a>\n  <a href=\'https://github.com/psf/black\'>\n    <img src=\'https://img.shields.io/badge/code%20style-black-000000.svg\' alt=\'Code style: black\' />\n  </a>\n</p>\n\n<p align="center">\n  <a href="#installation">Installation</a> •\n  <a href="#how-to-use">How To Use</a> •\n  <a href="#sample-sheet-image">Sheet</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#license">License</a>\n</p>\n\n<p align="center">This is a Python library that creates MNIST like training dataset for Handwritten Text Recognition related researches</p>\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install numiner.\n\n```bash\n$ pip install numiner\n```\n\nUse the package manager [pipenv](https://pypi.org/project/pipenv/) to install numiner.\n\n```bash\n$ pipenv install numiner\n```\n\nUse the package manager [poetry](https://pypi.org/project/poetry/) to install numiner.\n\n```bash\n$ poetry add numiner\n```\n\n## How To Use\n\nIn general, the package has two main modes. One is `sheet` and another one is `letter`.\n\n`sheet` - takes a path called `<source>` to a folder that\'s holding all the scanned _sheet_ images or an actual image path and saves the processed images in the `<result>` path\n\n```bash\n$ numiner -s/--sheet <source> <result>\n```\n\n`letter` - takes a path called `<source>` to a folder that\'s holding all the cropped raw images or an actual image path and saves the processed images in the `<result>` path\n\n```bash\n$ numiner -l/--letter <source> <result>\n```\n\nAlso you can override the default sheet labels by giving `json` file:\n\n```bash\n$ numiner --labels path/to/labels.json -s path/to/source path/to/result\n```\n\nFor sure you can also do this:\n\n```bash\n$ numiner --help\n\nusage: numiner [-h] [-v] [-s <source> <result>] [-l <source> <result>] [-c <path>]\n\noptional arguments:\n  -h, --help                    show this help message and exit\n  -v, --version                 show program\'s version number and exit\n  --clean <path>\n  -s/--sheet <source> <result>  a path to a folder or file that\'s holding the <source>\n                                sheet image(s) & a path to a folder where all <result>\n                                images will be saved\n  -l/--letter <source> <result> a path to a folder or a file that\'s holding the cropped\n                                image(s) & a path to a folder where all <result> images\n                                will be saved\n  --labels <path>               a path to .json file that\'s holding top to bottom, left\n                                to right labels of the sheet with their ids\n```\n\n```bash\n$ numiner convert --help\n\nusage: numiner convert [-h] -p <src> <dest> SIZE RATIO\n\npositional arguments:\n  SIZE                  number of images that each class contains\n  RATIO                 test, train or percentage of the test data\n                        in that case the rest of it will become\n                        train data\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p <src> <dest>, --paths <src> <dest>\n                        source and destination paths\n```\n\n## Sample Sheet image\n\n<p align="center">\n<img src="assets/sample_sheet.jpg" width="60%">\n</p>\n\nYou can also get the empty sheet file from [here](assets/sheet.pdf).\n\n## Extracted letters from the sheet\n\n<p align="center">\n<img src="assets/sheet_segmented.png">\n</p>\n\n## Final image processing order\n\nFollowed the same approach that EMNIST used when they were first creating their dataset from NIST SD images.\n\n1. Letter extracted from the sheet\n2. Binary version of original image\n3. Letter itself fitted into a square shape plus 2 pixel wide borders on each side without losing the aspect ratio\n4. From previous step, image resized to 28x28 and taken threshold results in final image\n\n<div align="center">\n  <img src="assets/letter_a_original.png" width="24%">\n  <img src="assets/letter_a_binary.png" width="24%">\n  <img src="assets/letter_a_cropped.png" width="24%">\n  <img src="assets/letter_a_final.png" width="24%">\n</div>\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\nIf you want to read more about how this project came to life, you can check out my [thesis report](https://github.com/khasbilegt/thesis-report/blob/master/main.pdf).\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Khasbilegt.TS',
    'author_email': 'khasbilegt.ts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/khasbilegt/numiner/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
