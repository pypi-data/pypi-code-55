# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="salt_cloud_module_kamatera",
    version="0.0.1",
    packages=find_packages(exclude=['tests',]),
    install_requires=["salt>=2019.2.0"],
    description='SaltStack Cloud module for managing Kamatera compute resources',
    author='Kamatera',
    url='https://github.com/Kamatera/salt-cloud-module-kamatera',
    license='MIT',
    entry_points={
        'salt.loader': [
            'cloud_dirs=salt_cloud_module_kamatera.loader:clouds_dirs',
        ],
    },
)
