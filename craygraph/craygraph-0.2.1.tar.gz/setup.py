"""
CRayGraph - a small toolkit for building dataflow-based framework
"""

from setuptools import setup, find_packages
import os

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description=f.read()

version = '0.2.1'

setup(
  name = 'craygraph',
  version=version,
  description="""A small toolkit for building dataflow-based framework.""",

  long_description=long_description,
  long_description_content_type="text/markdown",

  url='https://gitlab.com/craynn/craygraph',

  author='Maxim Borisyak and contributors.',
  author_email='maximus.been@gmail.com',

  maintainer='Maxim Borisyak',
  maintainer_email='maximus.been@gmail.com',

  license='MIT',

  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],

  packages=find_packages(exclude=['contrib', 'examples', 'docs', 'tests']),

  extras_require={
    'test': [
      'pytest>=4.0.0',
      'pytest-xdist>=1.31.0',
      'scipy>=1.3.0'
    ],
  },

  install_requires=[
    'pydotplus>=2.0.0',
  ],

  python_requires='>=3.7',
)


