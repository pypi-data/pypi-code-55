# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='cardsdk',
    version='0.4.9',
    description='CardSDK Scaffold CLI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='zhengchao zhang',
    author_email='chay0103@163.com',
    url='https://github.com/sopig',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[    
        'watchdog'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts':[
            'cardsdk = cardsdk.core:main'
        ]
    },
)

