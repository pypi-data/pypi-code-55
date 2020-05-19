# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clearscreen', 'clearscreen.art']

package_data = \
{'': ['*']}

install_requires = \
['colored>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['cls = clearscreen.cli:main']}

setup_kwargs = {
    'name': 'clearscreen',
    'version': '0.2.1',
    'description': 'Draws random ascii art to the screen, making it easier to scroll back and find where you where.',
    'long_description': "# ClearScreen (cls)\n\nThis is a replacement for CLS that is cross platform.\n\nInstead of clearing the screen, it shows a blob of random ascii art. Because the blob is always likely to be different, this makes it easy to scroll up and see where you were before your last command.\n\nThe ascii art comes from me, except for some old stuff used for the OpenStack Trove project.\n\nThis isn't to be confused with the [Inspect Class](https://pypi.org/project/cls/) package, which uses the package name cls (this uses the package name clearscreen).\n\nInstall with pipx or pipsi or whatever, then run:\n\n```bash\n    ? pipx install clearscreen\n    ? cls\n```\n\n\n## Change Log\n\n### 0.2.1\n\nAdds more art.\n\n### 0.2.0\n\nMakes showing different colors the default, cause hey why not. Also make the color selectable.\n\n### 0.1.1\n\nSorts order of files in the internal list to make it easier to find them with `--ls`.\n\n### 0.1.0\n\nFirst release.\n",
    'author': 'Tim Simpson',
    'author_email': 'timsimpson4@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TimSimpson/cls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
