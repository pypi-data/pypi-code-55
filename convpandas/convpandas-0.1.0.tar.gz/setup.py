# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convpandas', 'convpandas.command']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['convpandas = convpandas.__main__:cli']}

setup_kwargs = {
    'name': 'convpandas',
    'version': '0.1.0',
    'description': 'Convert file format with pandas',
    'long_description': '# convert-fileformat-with-pandas\nConvert file format with pandas\n',
    'author': 'yuji38kwmt',
    'author_email': 'yuji38kwmt@yahoo.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yuji38kwmt/convert-fileformat-with-pandas.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
