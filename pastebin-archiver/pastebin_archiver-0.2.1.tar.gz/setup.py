# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pastebin_archiver']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.6,<4.0', 'requests>=2.22,<3.0', 'sqlalchemy>=1.3,<2.0']

extras_require = \
{'mssql': ['pyodbc>=4.0,<5.0'],
 'mysql': ['pymysql>=0.9.3,<0.10.0'],
 'pgsql': ['psycopg2>=2.8,<3.0']}

entry_points = \
{'console_scripts': ['pastebin-archiver = pastebin_archiver.__main__:main']}

setup_kwargs = {
    'name': 'pastebin-archiver',
    'version': '0.2.1',
    'description': 'Archive all public posts from Pastebin.com',
    'long_description': "# Pastebin Archiver\n## What is this?\nThis app retrieves new posts made on Pastebin.com and stores them offline in a database. You can see the latest public posts it will retrieve [here](https://pastebin.com/archive).\n\n## Why?\nSome of the pastes posted to Pastebin contain interesting or sensitive data, and sometimes pastes are deleted by their poster or Pastebin staff. Running an instance of this archiver lets you retrieve deleted pastes and build a large dataset to run queries against.\n\n## Pastebin API info\n_Important:_ This archiver uses the [Pastebin Scraping API](https://pastebin.com/doc_scraping_api) which requires a whitelisted IP address and a Lifetime Pro account to use. [More info here](https://pastebin.com/faq#17).\n\n## Installation\n### Install from PyPI (recommended)\n1. Ensure you have Python 3.7+ installed.\n2. Run `pip install pastebin_archiver`\n3. Done! Jump down to the [Usage](#usage) section to get started.\n\n### Install from source\n1. Ensure you have Python 3.7+ and poetry installed\n    ```shell\n    $ python --version\n    Python 3.7.4\n    $ poetry --version\n    Poetry 0.12.17\n    ```\n2. Clone the git repository\n    ```shell\n    git clone https://gitlab.com/jonpavelich/pastebin-archiver.git \n    ```\n3. Install the dependencies\n    ```shell\n    $ cd pastebin-archiver\n    $ poetry install\n    ``` \n4. Run it!\n    ```shell\n    $ poetry run pastebin-archiver\n    ```\n\n### Run unit tests\n1. Install from source (see the section above)\n2. Run `poetry run python -m unittest`\n\n## Usage\n### Command line usage\nIf you installed the package using pip, then you can simply run `pastebin-archiver`: \n```shell\n$ pastebin-archiver         # Run with default settings\n$ pastebin-archiver --help  # Print available command line options\n```\n\n### Python usage \nIf you'd prefer to use the package in your own code, you can do so like this:\n```python\n# Import the package\nfrom pastebin_archiver import PastebinArchiver\n\n# (Optional) configure logging\nlogging.basicConfig(level=logging.DEBUG) \n\n# Run the application\napp = PastebinArchiver()\napp.main()\n```\n_Important:_ `app.main()` does not return, it runs forever looking for new pastes to fetch.\n\n## Configuration\nThe log target and log level can be controlled with options (`--logfile` and `--loglevel`) or environment variables (`LOG_FILE` and `LOG_LEVEL`).\n\n### Database\nBy default, the fetched data will be saved to a SQLite database file in your working directory called `pastebin.db`. You can change this behaviour by passing in a database connection string using the `--database` option or the `DATABASE` environment variable. For example:\n```shell\n$ pastebin-archiver --database 'postgresql://user:pass@localhost/mydatabase'\n```\n\n_Important:_ You'll need extra packages to connect to databases other than SQLite.\nFor PostgreSQL, you'll need to run `pip install psycopg2-binary` (or if you installed from source, you can run `poetry install -E pgsql`)\n\nFor detailed info on connection strings and a list of database packages you can use, see [the SQLAlchemy documentation](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls).\n\n## Contributing\nIf you find any bugs or have any suggestions to improve the project, please [open an issue](https://gitlab.com/jonpavelich/pastebin-archiver/issues/new) on GitLab.\n",
    'author': 'Jon Pavelich',
    'author_email': 'pypi@jonpavelich.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jonpavelich/pastebin-archiver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
