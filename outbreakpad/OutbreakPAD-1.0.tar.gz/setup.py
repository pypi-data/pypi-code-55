#!/usr/bin/env python
# coding=utf-8

from setuptools import  find_packages,setup
setup(
    name="OutbreakPAD",  
    version="1.0",
    author="Zou",
    author_email="21818662@zju.edu.cn",
    description=("This is a script of outbreak prediction"),
    license="GPLv3",
    keywords="Outbreak Prediction subscripe",
    url="https://github.com/FengYe-Lab/OutbreakPAD",
    packages=find_packages(),  #
    package_dir={ "OutbreakPAD": "OutbreakPAD" },
    package_data={"OutbreakPAD": ["exampledata/*.csv"]},
    test_suite="tests",

 
    install_requires=[
        'numpy>=1.7.0',
        'scipy',
        'pandas',
     #   'json',
        'statsmodels',
        'tensorflow',
        'neupy',
 #       'sklearn',
        'scikit-learn>=0.16.1',
        'matplotlib>=1.3.0'
    ],
    classifiers=[
    'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX :: Linux',
      'Operating System :: MacOS',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Topic :: Software Development :: Libraries :: Python Modules'],
  
    zip_safe=False
)
