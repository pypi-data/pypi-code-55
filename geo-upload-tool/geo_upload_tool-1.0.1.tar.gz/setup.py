#!/usr/bin/env python

from setuptools import setup, find_packages
import pkg_resources
import sys

# https://packaging.python.org/guides/single-sourcing-package-version/
with open('geo_upload_tool/version.py') as f :
    exec(f.read())

setup(name='geo_upload_tool',
      version=__version__
      ,description='CLI tool for preparing data submission to Gene Expression Omnibus'
      ,author='Adam Labadorf and the BU CAB Team'
      ,author_email='labadorf@bu.edu'
      ,install_requires=[
          'docopt',
          'future',
          'pandas',
          'setuptools',
          'pysam',
          'openpyxl'
          ]
      ,packages=find_packages()
      ,package_data={'':['*.snake'],'geo_upload_tool':['templates']}
      ,include_package_data=True
      ,entry_points={
        'console_scripts': [
          'gut=geo_upload_tool.geo_upload_tool:main'
        ]
      }
      ,setup_requires=[
        'pytest-runner'
       ]
      ,tests_require=['pytest']
      ,url='https://bitbucket.org/bucab/gut'
      ,license='MIT'
      ,classifiers=[
        'Development Status :: 3 - Alpha'
        ,'Intended Audience :: Science/Research'
        ,'Environment :: Console'
        ,'License :: OSI Approved :: MIT License'
        ,'Programming Language :: Python :: 3'
        ,'Topic :: Scientific/Engineering :: Bio-Informatics'
      ]
      ,keywords=['sequencing','NGS']
      ,python_requires='~=3.4'
     )
