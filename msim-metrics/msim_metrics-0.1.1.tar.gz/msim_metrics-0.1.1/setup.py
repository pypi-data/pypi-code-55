from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="msim_metrics",
    version="0.1.1",
    author="Jin",
    author_email="",
    description="Python Framework.",
    license="MIT",
    url="https://gitlab.momenta.works/jinpeng/msim_metrics",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
            'pandas>=0.20.0',
            'numpy>=1.14.0'
    ],
    zip_safe=True,
)
