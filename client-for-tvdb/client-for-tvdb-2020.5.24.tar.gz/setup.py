# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['client_for_tvdb']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.13.0,<0.14.0',
 'requests-cache>=0.5.2,<0.6.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'client-for-tvdb',
    'version': '2020.5.24',
    'description': 'A simple client for the TVDB API v3.',
    'long_description': '# client-for-tvdb\n\n[![CI](https://github.com/opacam/client-for-tvdb/workflows/CI/badge.svg?branch=develop)](https://github.com/opacam/client-for-tvdb/actions)\n[![codecov](https://codecov.io/gh/opacam/client-for-tvdb/branch/develop/graph/badge.svg)](https://codecov.io/gh/opacam/client-for-tvdb)\n[![Python versions](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat)](https://www.python.org/downloads/)\n[![GitHub release](https://img.shields.io/github/release/opacam/client-for-tvdb.svg)](https://gitHub.com/opacam/client-for-tvdb/releases/)\n[![GitHub tag](https://img.shields.io/github/tag/opacam/client-for-tvdb.svg)](https://gitHub.com/opacam/client-for-tvdb/tags/)\n[![PyPI version fury.io](https://badge.fury.io/py/client-for-tvdb.svg)](https://pypi.python.org/pypi/client-for-tvdb/)\n[![GitHub license](https://img.shields.io/github/license/opacam/client-for-tvdb.svg)](https://github.com/opacam/client-for-tvdb/blob/master/LICENSE.md)\n\n\nA simple client for the [Tvdb API v3](https://api.thetvdb.com/swagger).\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on your\nlocal machine for development and testing purposes. See deployment for notes on\nhow to deploy the project on a live system.\n\n### Prerequisites\n\n#### Tvdb Account\n\nYou will need an API key from TVDb.com to access the client. To obtain a\nkey, follow these steps:\n\n- 1. [Register](https://thetvdb.com/auth/register) for and verify an account.\n- 2. [Log into](https://thetvdb.com/auth/login) your account.\n- 3. [Fill your details](https://thetvdb.com/dashboard/account/apikey/create) to generate a new API key.\n\n#### Python Installation (recommended to use a virtual env)\n\nYou also need python >= 3.6 up and running. If your OS does not have the\nappropriate python version, you could install [pyenv](https://github.com/pyenv/pyenv) \nand create a virtual environment with the proper python version. Also you will\nneed an up to date pip installation (version `20.0.2` or greater is our\nrecommendation). So once you have `pyenv` installed\n(see [pyenv install instructions](https://github.com/pyenv/pyenv#installation)), \nmake an virtual environment for the project (we will use python version 3.8):\n\n```\npyenv virtualenv 3.8.1 client-for-tvdb\n```\n\nEnter inside the python environment we recently created (`client-for-tvdb`):\n```\npyenv activate client-for-tvdb\n```\n\nUpgrade `pip` package:\n```\npip install --upgrade pip\n```\n\nInstall `poetry` package:\n```\npip install poetry\n```\n\n### Installing\n\nOnce you have the prerequisites installed, you can proceed installing the\nproject. The project uses an `pyproject.toml` file to manage the installation\n(PEP517) and also we will make use of the python package\n[poetry](https://github.com/python-poetry/poetry) as our `build-system`\n(PEP518). So, to do the install you only need to `cd` to the\nproject folder:\n\n```\ncd client-for-tvdb\n```\n\nAnd run the install of the dependencies via `poetry` command:\n\n```\npoetry install\n```\n\n\n## Running API client\n\nTo use this tvdb API client, first you must initialize the client with\nthe proper credentials:\n\n```python\nfrom client_for_tvdb import TvdbClient\n\ntvdb_client = TvdbClient(\n    user_name="Your user name",\n    user_key="Your user key",\n    api_key="Your API key"\n)\n```\n\nAlso you could setup your credentials via environment variables, wrote\nin `.env` file which should be located inside the `client_for_tvdb`\nmodule (or you could `export` them):\n```\nTVDB_USER_NAME=<Your user name>\nTVDB_USER_KEY=<Your user key>\nTVDB_API_KEY=<Your API key>\n```\n\nYou can perform the following queries, assuming that you have setup your\ncredentials via `.env` file:\n\n- To get a list of possible matching tvshows:\n  ```python\n  from client_for_tvdb import TvdbClient\n\n  tvdb_client = TvdbClient()\n  # get a list of dictionaries with tvshows from the TVDB API\n  search_result = tvdb_client.search("Game of Thrones")\n  ```\n\n- To get only the closest matching tvshow:\n  ```python\n  from client_for_tvdb import TvdbClient\n\n  tvdb_client = TvdbClient()\n  # will return a dictionary\n  search_result = tvdb_client.search_closest_matching("Game of Thrones")\n  ```\n\n- You also could perform a query supplying a `tvdb_id`\n  ```python\n  from client_for_tvdb import TvdbClient\n\n  tvdb_client = TvdbClient()\n  # will return a dictionary\n  search_result = tvdb_client.get_serie_by_id(121361)\n  ```\n\n## Running the tests\n\nTo run our project tests you can use `pytest` with coverage:\n\n```\nPYTHONPATH=. pytest tests/ --cov client_for_tvdb/\n```\n\n## Built With\n\n* [Python 3](https://docs.python.org/3/) - The programming language\n* [Poetry](https://python-poetry.org/docs/) - Dependency Management\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of\nconduct, and the process for submitting pull requests to us.\n\n## Versioning\n\nWe use [CalVer](https://calver.org/) for versioning. For the versions available,\nsee the [tags on this repository](https://github.com/opacam/client-for-tvdb/tags).\n\n\n## Authors\n\n* **Pol Canelles** - *Initial work* - [opacam](https://github.com/opacam)\n\nSee also the list of [contributors](https://github.com/opacam/client-for-tvdb/contributors)\nwho participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n\n## Acknowledgments\n\n* [Tvdb API docs](https://api.thetvdb.com/swagger)\n',
    'author': 'opacam',
    'author_email': 'canellestudi@gmail.com',
    'maintainer': 'opacam',
    'maintainer_email': 'canellestudi@gmail.com',
    'url': 'https://github.com/opacam/client-for-tvdb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
