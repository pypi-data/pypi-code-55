# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_image_tool']

package_data = \
{'': ['*'], 'simple_image_tool': ['template/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'Pillow>=7.1.2,<8.0.0',
 'boto3>=1.13.11,<2.0.0',
 'flask>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['simple-image-tool = simple_image_tool:main']}

setup_kwargs = {
    'name': 'simple-image-tool',
    'version': '0.0.2',
    'description': 'A simple command line tool to upload new image or view existing images on s3',
    'long_description': None,
    'author': 'Jiaming Shang',
    'author_email': 'shangjiaming.yuan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sjmyuan/simple-image-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
