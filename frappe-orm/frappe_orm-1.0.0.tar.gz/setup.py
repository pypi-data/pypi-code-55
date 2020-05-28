import setuptools
import os

# from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

version = '1.0.0'

setuptools.setup(name='frappe_orm',
                 packages=setuptools.find_packages(),
                 version=version,
                 description='Frappe Framework Orm',
                 author='omar hamdy',
                 author_email='omarhamdy49@gmail.com',
                 license='MIT',
                 keywords=["frappe", "orm", "postgres", "mariadb", "database"],
                 zip_safe=False)
