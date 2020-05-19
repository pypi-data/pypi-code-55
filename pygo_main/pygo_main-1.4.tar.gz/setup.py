# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe: 

usage:

------------------------------------------------
"""
from setuptools import setup, find_packages

setup(
    name="pygo_main",
    version="1.4",
    keywords=["main", "pygo", "python2"],
    description="python project sdk",
    long_description="this is the python project sdk by pygo to develop",
    license="MIT Licence",

    url="http://pygo2.cn",
    author="pygo",
    author_email="gaoming971366@163.com",

    packages=find_packages(),
    py_modules=[],
    include_package_data=True,
    platforms="any",

    scripts=[],
    python_requires=">=2.7",
    install_requires=[
        "setuptools>=16.0"
    ],
    entry_points={
        'console_scripts': [
            'pygo_fooo = main.cli:fooo'
        ]
    }
)
