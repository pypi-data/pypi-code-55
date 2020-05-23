# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solists']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'solists',
    'version': '0.1.7',
    'description': 'Implementation of self-organizing lists.',
    'long_description': '# sol\n\nImplementation of [self-organizing](https://en.wikipedia.org/wiki/Self-organizing_list) linked lists.\n\n[![CodeFactor](https://www.codefactor.io/repository/github/vsevolodbazhan/sol/badge)](https://www.codefactor.io/repository/github/vsevolodbazhan/sol)\n[![Codecov](https://codecov.io/gh/vsevolodbazhan/Sol/branch/master/graph/badge.svg)](https://codecov.io/gh/vsevolodbazhan/sol)\n![License](https://img.shields.io/github/license/vsevolodbazhan/sol)\n\n## Installation\n\n```bash\npip install solists\n```\n\n## Documentation\n\nDocumentation is available online at https://vsevolodbazhan.github.io/sol/ and in the `docs` directory.\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate and run existing ones using:\n\n```bash\nmake test\n```\n\n## License\n\n[MIT](https://github.com/vsevolodbazhan/sol/blob/master/LICENSE)\n',
    'author': 'Vsevolod Bazhan',
    'author_email': 'vsevozhan@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vsevolodbazhan/Sol',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
