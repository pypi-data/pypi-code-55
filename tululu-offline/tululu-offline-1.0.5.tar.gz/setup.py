# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tululu_offline']

package_data = \
{'': ['*'],
 'tululu_offline': ['template/*',
                    'template/images/*',
                    'template/static/css/*',
                    'template/static/js/*']}

install_requires = \
['BeautifulSoup4>=4.8.2,<5.0.0',
 'Jinja2>=2.11.1,<3.0.0',
 'livereload>=2.6.1,<3.0.0',
 'lxml>=4.5.0,<5.0.0',
 'more-itertools>=8.3.0,<9.0.0',
 'pathvalidate>=2.2.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.43.0,<5.0.0']

entry_points = \
{'console_scripts': ['tululu-offline = tululu_offline.app:main']}

setup_kwargs = {
    'name': 'tululu-offline',
    'version': '1.0.5',
    'description': 'Read it tululu.org without Internet',
    'long_description': '# Save the category of site tululu.org offline\n\n<p align="center">\n    <img width="500"\n         src="http://omsklib.ru/files/news/2017/predvarit-zakaz/166513214-1.jpg"\n         alt="Books library restyle" />\n</p>\n\n## Description\n[![Maintainability](https://api.codeclimate.com/v1/badges/c8ec73b47d297795daae/maintainability)](https://codeclimate.com/github/velivir/tululu-offline/maintainability)\n[![Build Status](https://travis-ci.com/velivir/tululu-offline.svg?branch=master)](https://travis-ci.com/velivir/tululu-offline)\n[![Coverage Status](https://coveralls.io/repos/github/velivir/tululu-offline/badge.png?branch=master)](https://coveralls.io/github/velivir/tululu-offline?branch=master)\n![Platform](https://img.shields.io/badge/platform-linux-brightgreen)\n![Python_versions](https://img.shields.io/badge/Python-3.7%7C3.8-brightgreen)\n![GitHub](https://img.shields.io/github/license/velivir/books-library-restyle)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\nThe program downloads from [tululu.org](http://tululu.org/) books in text format and their covers. The following information is also downloaded to the json file:\n- title;\n- author;\n- image path;\n- book path;\n- comments;\n- genres.\n\nAfter downloading the necessary data, the offline version of the site will be generated (you can see an example [here](https://velivir.github.io/tululu-offline/pages/index1.html)).\n\n\n## Table of content\n\n- [Installation](#installation)\n- [How to use](#how-to-use)\n- [Options](#options)\n- [Example run](#example-run)\n- [For developers](#for-developers)\n    - [How to install with dev dependencies](#how-to-install-with-dev-dependencies)\n    - [How to run](#how-to-run)\n    - [Example of running a script](#example-of-running-a-script)\n    - [Start render website](#start-render-website)\n    - [How to run lint files](#how-to-run-lint-files)\n    - [How to run tests](#how-to-run-tests)\n- [License](#license)\n- [Project goal](#project-goal)\n\n\n## Installation\n\nInstall using [pip](https://pypi.org/project/tululu-offline/):\n  ```bash\n  pip install tululu-offline\n  ```\n\n## How to use\n\n  ```bash\n  tululu-offline [OPTIONS]\n  ```\n\n## Options\n\n- `category_url` - the category url [tululu.org](http://tululu.org);\n- `--start_page` - which page to start downloading;\n- `--end_page` - on which page to finish downloading;\n- `--dest_folder` - path to the directory with parsing results: pictures, books, JSON;\n- `--skip_txt` - do not download books;\n- `--skip_imgs` - do not download images;\n- `--json_path` - specify your path to *.json file with results;\n- `--number_of_books_per_page` - number of books per page.\n\n## Example run\n\nRun the script with the necessary parameters. For example:\n```bash\ntululu-offline http://tululu.org/l55/ --start_page 1 --end_page 3 --skip_txt true --skip_imgs true --number_of_books_per_page 15\n```\n\nThe first page of the library will be available at ```pages/index1.html```.\n\n\n## For developers\n\n### How to install with dev dependencies\n\nInstall using [poetry](https://python-poetry.org/):\n```bash\ngit clone https://github.com/velivir/tululu-offline\ncd tululu-offline\nmake install_dev\n```\n\n### How to run:\n\n```bash\npoetry run python3 tululu_offline/app.py [OPTIONS]\n```\n\n### Example of running a script\n\n```bash\npoetry run python3 tululu_offline/app.py http://tululu.org/l55/ --start_page 1 --end_page 5 --skip_txt true --skip_imgs true --number_of_books_per_page 10\n```\n\n### Start render website\n\nRun the file `render_website.py` with the following options:\n\n- `category_url` - the category url [tululu.org](http://tululu.org);\n- `--dest_folder` - path to the directory with parsing results: pictures, books, JSON;\n- `--json_path` - specify your path to *.json file with results;\n- `--number_of_books_per_page` - number of books per page.\n\nExample:\n```bash\npoetry run python3 tululu_offline/render_website.py http://tululu.org/l55/ --number_of_books_per_page 10 --json_path result/books.json --dest_folder result\n```\n\n### How to run lint files\n\n```bash\nmake lint\n```\n\n### How to run tests\n\n```bash\nmake test\n```\n\n## License\n\nTululu-offline is licensed under the MIT License. See [LICENSE](https://github.com/velivir/tululu-offline/blob/master/LICENSE) for more information.\n\n## Project goal\n\nThe code is written for educational purposes in an online course for web developers [dvmn.org](https://dvmn.org).\n',
    'author': 'Vitaliy Antonov',
    'author_email': 'vitaliyantonoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/velivir/tululu-offline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
