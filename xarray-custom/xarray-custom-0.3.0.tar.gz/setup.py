# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_custom']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'xarray>=0.15,<0.16']

setup_kwargs = {
    'name': 'xarray-custom',
    'version': '0.3.0',
    'description': 'Data classes for custom xarray constructors',
    'long_description': '# xarray-custom\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-custom.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/xarray-custom/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-custom.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/xarray-custom/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/xarray-custom/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/xarray-custom/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\n:zap: Data classes for custom xarray constructors\n\n## TL;DR\n\nxarray-custom is a third-party Python package which helps to create custom DataArray classes in the same manner as [the Python\'s native dataclass](https://docs.python.org/3/library/dataclasses.html).\nHere is an introduction code of what the package provides:\n\n```python\nfrom xarray_custom import ctype, dataarrayclass\n\n@dataarrayclass(accessor=\'img\')\nclass Image:\n    """DataArray class to represent images."""\n\n    dims = \'x\', \'y\'\n    dtype = float\n    x: ctype(\'x\', int) = 0\n    y: ctype(\'y\', int) = 0\n\n    def normalize(self):\n        return self / self.max()\n\n# create a custom DataArray\nimage = Image([[0, 1], [2, 3]], x=[0, 1], y=[0, 1])\n\n# use a custom method via an accessor\nnormalized = image.img.normalize()\n\n# create a custom DataArray filled with ones\nones = Image.ones((2, 2), x=[0, 1], y=[0, 1])\n```\n\nThe key points are:\n\n- Custom DataArray instances with fixed dimensions, datatype, and coordinates can easily be created.\n- NumPy-like special functions like ``ones()`` are provided as class methods.\n- Custom DataArray methods can be available via a custom accessor.\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/xarray-custom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
