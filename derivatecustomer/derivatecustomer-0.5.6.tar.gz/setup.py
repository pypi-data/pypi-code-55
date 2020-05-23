# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['derivatecustomer']
install_requires = \
['click-help-colors>=0.6,<0.7',
 'click>=7.0,<8.0',
 'dulwich>=0.19.13,<0.20.0',
 'git-url-parse>=1.2.2,<2.0.0',
 'logbook>=1.5.3,<2.0.0',
 'single-version>=1.1,<2.0',
 'unidecode>=1.1.1,<2.0.0',
 'vistickedword>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'derivatecustomer',
    'version': '0.5.6',
    'description': 'AgriConnect internal tool to make a derivation of PlantingHouse for customer',
    'long_description': '================\nDerivateCustomer\n================\n\n`AgriConnect`_ internal tool to make a derivation of PlantingHouse for customer.\n\nUsage\n-----\n\n- Fork the PlantingHouse repo.\n- Go to "Settings > General > Change path", change to customer codename.\n- Run the command, passing forked repo URL. Example:\n\n.. code-block:: sh\n\n    python3 -m derivatecustomer -g git@gitlab.com:quan/phuc-daothanh.git -n "Phúc Đạo Thạnh" -s fa\n\n- To learn about this tool\'s options, run with ``--help``:\n\n.. code-block:: sh\n\n    python3 -m derivatecustomer --help\n\n\n.. _agriconnect: https://agriconnect.vn\n',
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/agriconnect/tools/derivatecustomer',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
