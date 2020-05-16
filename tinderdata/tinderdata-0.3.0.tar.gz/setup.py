# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinderdata']

package_data = \
{'': ['*']}

install_requires = \
['fsbox>=0.2.0,<0.3.0',
 'loguru>=0.4,<0.5',
 'matplotlib>=3.2,<4.0',
 'pandas>=0.25,<0.26',
 'seaborn>=0.10,<0.11']

setup_kwargs = {
    'name': 'tinderdata',
    'version': '0.3.0',
    'description': 'A silly utility to explore your Tinder data.',
    'long_description': '# Tinderdata: Get insight on your Tinder user data.\n\nA very simple package to mine your Tinder user data, and get insight on your time on the service.\n\n## Install\n\nThis code is compatible with `Python 3.6+`.\nIf for some reason you have a need for it, you can simply install it in your virtual enrivonment with:\n```bash\npip install tinderdata\n```\n\n## Usage\n\nThe script parses arguments from the commandline.\nThe usage goes as:\n\n```\npython -m tinder_data [-h] -p PATH [--show-figures SHOW] [--save-figures SAVE] [-l LOG_LEVEL]\n```\n\nThe different options are as follows:\n```\nusage: __main__.py [-h] -p PATH [--show-figures SHOW] [--save-figures SAVE]\n                   [-l LOG_LEVEL]\n\nGetting insight on your Tinder usage.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PATH, --path-to-data PATH\n                        Absolute path to the json file of your tinder data.\n                        Can be absolute or relative.\n  --show-figures SHOW   Whether or not to show figures when plotting insights.\n                        Defaults to False.\n  --save-figures SAVE   Whether or not to save figures when plotting insights.\n                        Defaults to False.\n  -l LOG_LEVEL, --logs LOG_LEVEL\n                        The base console logging level. Can be \'debug\',\n                        \'info\', \'warning\' and \'error\'. Defaults to \'info\'.\n```\n\nAn example command is then:\n```\npython -m tinderdata -p path_to_tinderdata.json --logs debug --save-figures True\n```\n\nThe script print out a number of insight statements, and finally the text you should paste to get a Sankey diagram.\nIt will then create a `plots` folder and populate it with visuals.\n\nYou can otherwise import the high-level object from the package, and use at your convenience:\n```python\nfrom tinderdata import TinderData\n\ntinder = TinderData("tinderdata.json")\ntinder.output_sankey_string()\ntinder.plot_messages_loyalty(showfig=True, savefig=False)\n```\n\n## Output example\n\nHere are examples of the script\'s outputs:\n<p align="center">\n  <img src="https://github.com/fsoubelet/Tinder_Data/blob/master/plots/messages_monthly_stats.png"/>\n</p>\n\n<p align="center">\n  <img src="https://github.com/fsoubelet/Tinder_Data/blob/master/plots/swipes_weekdays_stats.png"/>\n</p>\n\n## License\n\nCopyright &copy; 2019-2020 Felix Soubelet. [MIT License][license]\n\n[license]: https://github.com/fsoubelet/Tinder_Data/blob/master/LICENSE',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/Tinder_Data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
