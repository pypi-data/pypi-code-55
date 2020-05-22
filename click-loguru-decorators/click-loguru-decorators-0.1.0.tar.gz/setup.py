#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io

from setuptools import setup

setup(
    name='click-loguru-decorators',
    version='0.1.0',
    description="""Easy integration of Click and loguru""",
    long_description=io.open("README.md", 'r', encoding="utf-8").read(),
    url='https://github.com/illagrenan/click-loguru-decorators',
    license='MIT',
    author='Vasek Dohnal',
    author_email='vaclav.dohnal@gmail.com',
    packages=['click_loguru'],
    install_requires=['loguru', 'Click'],
    python_requires='~=3.8',
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent'
    ]
)
