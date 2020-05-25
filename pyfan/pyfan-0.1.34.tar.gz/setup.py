# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfan', 'pyfan.util', 'pyfan.util.path', 'pyfan.util.pdf', 'pyfan.util.rmd']

package_data = \
{'': ['*']}

install_requires = \
['python-frontmatter>=0.5.0,<0.6.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'pyfan',
    'version': '0.1.34',
    'description': '',
    'long_description': None,
    'author': 'Fan Wang',
    'author_email': 'wangfanbsg75@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
