#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
from setuptools import find_packages

name = 'ProfitDataFrame'
version = '2020.5.26'
author = 'Zhang Chuanpeng'
author_email = 'yz7zzxj001@qq.com'
description = '''This is a package for myself to make data analysis easily, it includes some functions 
which only work with pandas.DataFrame.\n
'''
long_description = 'This is a package for myself to make data analysis easily'
install_requires = ['pandas','numpy']

setup(name = name
        , version = version
        ,long_description = long_description
        ,author = author
        ,author_email = author_email
        ,description = description
        ,install_requires = install_requires
        ,keywords='data analysis tools'
        ,packages = find_packages('src')
        ,package_dir = {'':'src'}
        ,include_package_data = True
        ,url = ''
        )  

