# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xcat']

package_data = \
{'': ['*']}

install_requires = \
['aiodns',
 'aiohttp>=3.0.0,<4.0.0',
 'appdirs',
 'cchardet',
 'click',
 'colorama',
 'prompt-toolkit<4',
 'xpath-expressions>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['xcat = xcat.cli:cli']}

setup_kwargs = {
    'name': 'xcat',
    'version': '1.1.0',
    'description': 'A command line tool to automate the exploitation of blind XPath injection vulnerabilities',
    'long_description': '# XCat\n\n![Python package](https://github.com/orf/xcat/workflows/Python%20package/badge.svg)\n![](https://img.shields.io/pypi/v/xcat.svg)\n![](https://img.shields.io/pypi/l/xcat.svg)\n![](https://img.shields.io/pypi/pyversions/xcat.svg)\n\nXCat is a command line tool to exploit and investigate blind XPath injection vulnerabilities.\n\nFor a complete reference read the documentation here: https://xcat.readthedocs.io/en/latest/\n\nIt supports an large number of features:\n\n- Auto-selects injections (run `xcat injections` for a list)\n\n- Detects the version and capabilities of the xpath parser and\n  selects the fastest method of retrieval\n\n- Built in out-of-bound HTTP server\n    - Automates XXE attacks\n    - Can use OOB HTTP requests to drastically speed up retrieval\n\n- Custom request headers and body\n\n- Built in REPL shell, supporting:\n    - Reading arbitrary files\n    - Reading environment variables\n    - Listing directories\n    - Uploading/downloading files (soon TM)\n\n- Optimized retrieval\n    - Uses binary search over unicode codepoints if available\n    - Fallbacks include searching for common characters previously retrieved first\n    - Normalizes unicode to reduce the search space\n\n## Install\n\nRun `pip install xcat`\n\n**Requires Python 3.7**. You can easily install this with [pyenv](https://github.com/pyenv/pyenv):\n`pyenv install 3.7.1`\n\n## Example application\n\nThere is a complete demo application you can use to explore the features of XCat.\nSee the README here: https://github.com/orf/xcat_app\n\n',
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/orf/xcat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
