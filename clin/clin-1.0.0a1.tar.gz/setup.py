# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clin', 'clin.models']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'deepdiff>=4.3.2,<5.0.0',
 'pygments>=2.6.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['clin = clin.run:cli']}

setup_kwargs = {
    'name': 'clin',
    'version': '1.0.0a1',
    'description': 'Cli for Nakadi resources management in infrastructure-as-a-code manner',
    'long_description': '# Clin\n\n**Clin** is a command-line utility to manage [Nakadi](https://nakadi.io/)\nresources from schema files in "Infrastructure-as-a-Code" style.\n![](/docs/gifs/demo.gif)\n\n## User Guide\n\n### Prerequisites\n\n* [Python](https://www.python.org/) >= 3.7\n\n### Installing\nYou can install **clin** direcly from [PyPI](https://pypi.org/project/clin/)\nusing pip:\n\n```bash\npip install clin\n```\n\n### Getting started\n\nAfter this you should be able to run tool:\n```bash\n~ clin --help\nUsage: clin [OPTIONS] COMMAND [ARGS]...\n...\n```\n\nPlease refer [documentation](/docs) and [examples](/docs/examples)\n\n## Contributing\n\nPlease read [CONTRIBUTING](CONTRIBUTING.md) for details on our process for\nsubmitting pull requests to us, and please ensure you follow the\n[CODE_OF_CONDUCT](CODE_OF_CONDUCT.md).\n\n### Prerequisites\n\n* [Python](https://www.python.org/) >= 3.7\n* [Poetry](https://python-poetry.org/) for packaging and dependency\n  management. See the [official docs](https://python-poetry.org/docs/) for\n  instructions on installation and basic usage.\n\n### Installing\nAfter cloning the repository, use `poetry` to create a new virtual environment\nand restore all dependencies.\n\n```bash\npoetry install\n```\n\nIf you\'re using an IDE (eg. PyCharm), make sure that it\'s configured to use the\nvirtual environment created by poetry as the project\'s interpreter. You can find\nthe path to the used environment with `poetry env info`.\n\n### Running the tests\n\n```bash\npoetry run pytest\n```\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available,\nsee the [tags on this repository](https://github.com/zalando-incubator/clin/tags).\n\n## Authors\n\n* **Dmitry Erokhin** [@Dmitry-Erokhin](https://github.com/Dmitry-Erokhin)\n* **Daniel Stockhammer** [@dstockhammer](https://github.com/dstockhammer)\n\nSee also the list of [contributors](CONTRIBUTORS.md) who participated in this\nproject.\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE)\nfile for details.\n',
    'author': 'Dmitry Erokhin',
    'author_email': 'dmitry.erokhin@zalando.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.bus.zalan.do/derokhin/clin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
