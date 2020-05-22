# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['x_ae_a_12']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.6.0,<4.0.0',
 'pytest-mock>=3.1.0,<4.0.0',
 'requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['x-ae-a-12 = x_ae_a_12.console:main']}

setup_kwargs = {
    'name': 'x-ae-a-12',
    'version': '0.2.0',
    'description': 'The X-AE-A-12 Python project',
    'long_description': '# X-AE-A-12\n\n[![Tests](https://github.com/SpencerOfwiti/X-AE-A-12/workflows/Tests/badge.svg)](https://github.com/SpencerOfwiti/X-AE-A-12/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/SpencerOfwiti/X-AE-A-12/branch/master/graph/badge.svg)](https://codecov.io/gh/SpencerOfwiti/X-AE-A-12)\n[![PyPI](https://img.shields.io/pypi/v/x-ae-a-12.svg)](https://pypi.org/project/x-ae-a-12/)\n[![Read the Docs](https://readthedocs.org/projects/x-ae-a-12/badge/)](https://x-ae-a-12.readthedocs.io/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n![GitHub repo size](https://img.shields.io/github/repo-size/SpencerOfwiti/X-AE-A-12.svg)\n![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)\n[![contributors](https://img.shields.io/github/contributors/SpencerOfwiti/X-AE-A-12.svg)](https://github.com/SpencerOfwiti/X-AE-A-12/contributors)\n\nCommand line application for displaying random facts from wikipedia on the console.\nAvailable as a python package on PyPI:\n```\npip install x-ae-a-12\n```\nDocumentation available at: [X-AE-A-12 docs](https://x-ae-a-12.readthedocs.io/en/latest/)\n\n## Table of contents\n* [Built With](#built-with)\n* [Features](#features)\n* [Code Example](#code-example)\n* [Prerequisites](#prerequisites)\n* [Installation](#installation)\n* [Tests](#tests)\n* [Deployment](#deployment)\n* [Contributions](#contributions)\n* [Bug / Feature Request](#bug--feature-request)\n* [Authors](#authors)\n* [License](#license)\n\n## Built With\n* [Python 3.8](https://www.python.org/) - The programming language used.\n* [Poetry](https://python-poetry.org/) - The dependency manager used.\n* [Nox](https://nox.thea.codes/en/stable/) - The automation tool used.\n* [Pytest](https://docs.pytest.org/en/latest/) - The testing framework used.\n* [Flake8](https://flake8.pycqa.org/en/latest/) - The linting tool used.\n* [Sphinx](https://www.sphinx-doc.org/en/master/) - The documentation generator used.\n* [GitHub Actions](https://github.com/actions) - CI-CD tool used.\n\n## Features\n\n- Display random facts from Wikipedia.\n- Select Wikipedia language edition to be used.\n\n## Code Example\n\n```python\ndef main(language: str) -> None:\n    """The X-AE-A-12 Python project."""\n    page = wikipedia.random_page(language=language)\n\n    click.secho(page.title, fg="green")\n    click.echo(textwrap.fill(page.extract))\n```\n\n## Prerequisites\n\nWhat things you need to install the software and how to install them\n\n* **python 3.8**\n\nLinux:\n```\nsudo apt-get install python3.8\n```\n\nWindows:\n\nDownload from [python.org](https://www.python.org/downloads/windows/)\n\nMac OS:\n```\nbrew install python3\n```\n\n* **pip**\n\nLinux and Mac OS:\n```\npip install -U pip\n```\n\nWindows:\n```\npython -m pip install -U pip\n```\n\n* **poetry**\n```\ncurl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n```\n\n* **nox**\n```\npip install --user --upgrade nox\n```\n\n## Installation\n\nClone this repository:\n```\ngit clone https://github.com/SpencerOfwiti/X-AE-A-12\n```\n\nTo set up virtual environment and install dependencies:\n```\npoetry install\n```\n\nTo run application:\n```\npoetry run x-ae-a-12\n```\n\n## Tests\n\nThis system uses pytest to run automated tests.\n\nTo run automated tests:\n```\nnox -s tests\n```\n\n## Deployment\n\nTo deploy application on PyPI(Python Package Index):\n```\npoetry build\n```\n\n```\npoetry publish\n```\n\n## Contributions\n\nTo contribute, follow these steps:\n\n1. Fork this repository.\n2. Create a branch: `git checkout -b <branch_name>`.\n3. Make your changes and commit them: `git commit -m \'<commit_message>\'`\n4. Push to the original branch: `git push origin <project_name>/<location>`\n5. Create the pull request.\n\nAlternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).\n\n\n## Bug / Feature Request\n\nIf you find a bug (the website couldn\'t handle the query and / or gave undesired results), kindly open an issue [here](https://github.com/SpencerOfwiti/X-AE-A-12/issues/new) by including your search query and the expected result.\n\nIf you\'d like to request a new function, feel free to do so by opening an issue [here](https://github.com/SpencerOfwiti/X-AE-A-12/issues/new). Please include sample queries and their corresponding results.\n\n## Authors\n\n* **[Spencer Ofwiti](https://github.com/SpencerOfwiti)** - *Initial work*\n\n[![github follow](https://img.shields.io/github/followers/SpencerOfwiti?label=Follow_on_GitHub)](https://github.com/SpencerOfwiti)\n[![twitter follow](https://img.shields.io/twitter/follow/SpencerOfwiti?style=social)](https://twitter.com/SpencerOfwiti)\n\nSee also the list of [contributors](https://github.com/SpencerOfwiti/X-AE-A-12/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details\n',
    'author': 'Spencer Ofwiti',
    'author_email': 'maxspencer56@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SpencerOfwiti/X-AE-A-12',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
