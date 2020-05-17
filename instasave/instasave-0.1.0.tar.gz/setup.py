# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instasave']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.4.1,<0.5.0', 'requests>=2.23.0,<3.0.0', 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'instasave',
    'version': '0.1.0',
    'description': 'Download script for Instagram posts',
    'long_description': '<h1 align="center">\n  <b>instasave</b>\n</h1>\n\nA simple script to download media from Instagram posts.\n\n## Install\n\nThis script runs on Python3.6+, and requires the following libraries: [`requests`][requests_url], [`tqdm`][tqdm_url] and [`loguru`][loguru_url].\nYou can install this package from PyPI with:\n```bash\npip install instasave\n```\n\n## Usage\n\nWith this package is installed in the activated enrivonment, usage is:\n```bash\npython -m instasave --url link_to_instagram_post\n```\n\nDetailed options go as follows:\n```bash\nusage: __main__.py [-h] -u URL [-l LOG_LEVEL]\n\nDownloading media from Instagram posts.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -u URL, --url URL     Link to the Instagram post you want to download the\n                        content of.\n  -l LOG_LEVEL, --logs LOG_LEVEL\n                        The base console logging level. Can be \'debug\',\n                        \'info\', \'warning\' and \'error\'. Defaults to \'info\'.\n```\n\nThe downloaded files will be saved in the current directory under a name composed of the file type (image / video) appended by the download timestamp.\n\nWarning: abusing this script may get your IP banned by Instagram.\n\n## TODO\n\n- [x] Implement proper logging.\n- [x] Make into a package.\n- [x] Make callable as a python module (`python -m instasave ...`).\n\n## License\n\nCopyright &copy; 2020 Felix Soubelet. [MIT License][license]\n\n[loguru_url]: https://github.com/Delgan/loguru\n[requests_url]: https://github.com/psf/requests\n[tqdm_url]: https://github.com/tqdm/tqdm',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/InstaSave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
