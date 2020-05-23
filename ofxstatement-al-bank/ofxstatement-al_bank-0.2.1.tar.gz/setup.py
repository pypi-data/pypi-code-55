#!/usr/bin/python3

from distutils.core import setup

from setuptools import find_packages

version = "0.2.1"

with open('README.rst') as f:
    long_description = f.read()

setup(name='ofxstatement-al_bank',
      version=version,
      author="Leonardo Brondani Schenkel",
      author_email="leonardo@schenkel.net",
      url="https://github.com/lbschenkel/ofxstatement-al_bank",
      description="Arbejdernes Landsbank plugin for ofxstatement",
      long_description=long_description,
      license="GPLv3",
      keywords=["ofx", "banking", "statement"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          'ofxstatement': ['al_bank = ofxstatement.plugins.al_bank:ALBankPlugin']
      },
      install_requires=['ofxstatement'],
      include_package_data=True,
      zip_safe=True
      )
