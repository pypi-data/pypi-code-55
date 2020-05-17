# -*- coding: utf-8 -*-
import setuptools

exec(open('pysparkfgdevbi/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    #'lxml>=4.3.4',
    #'mock>=2.0.0,<3.0.0',
    #'pytest>=3.0.6,<4.0.0',
    #'pytest-cov>=2.4.0,<3.0.0',
    #'pylama>=7.4.1,<8.0.0',
    #'cython>=0.29.12',
    #'numpy>=1.16.4',
    #'scipy>=1.3.0',
    #'scikit-learn>=0.21.2'
]

setuptools.setup(
    name="pysparkfgdevbi",
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FG239/pysparkfgdevbi',
    license='gpl-3.0',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
)