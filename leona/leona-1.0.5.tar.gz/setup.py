import os
from codecs import open
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requires = f.read()

setup(
    name="leona",
    version='1.0.5',
    author="Juan Guillermo Escalona",
    author_email="j.escalona@hlcn.mx",
    url="https://bitbucket.org/hlcn/leona",
    description='CLI for DevOps Integration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['leona'],
    zip_safe=False,
    packages=find_packages(),
    data_files=None,
    python_requires='>=3.7.6',
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'leona=src.leona:cli',
        ],
    },
)
