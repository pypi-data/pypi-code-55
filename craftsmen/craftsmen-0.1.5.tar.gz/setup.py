#! /usr/bin/env python
from setuptools import setup, find_packages
from src.craftsmen import __version__

setup(
    name='craftsmen',
    version=__version__,
    packages=find_packages('src', exclude=('test*', 'examples')) +['craftsmen/curry'],
    package_dir={'': 'src'},
    include_package_data=True,
    platforms='any',
    license='MIT',
    description = 'craftsmen description',
    # long_description = 'craftsmen description',
    author = 'heyderpd',
    author_email = 'heyderpd@gmail.com',
    # cmdclass={'test': PyTest,},
    url = 'https://github.com/heyderpd/pypi-craftsmen',
    download_url = f'https://github.com/heyderpd/pypi-craftsmen/dist/craftsmen-{__version__}.tar.gz',
    keywords = ['ramda', 'utils', 'functional'],
    tests_require=[],
    install_requires=[],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.8',
    ],
    # classifiers = [
    #   'Programming Language :: Python',
    #   'Natural Language :: English',
    #   'Operating System :: OS Independent',
    #   'Topic :: Software Development :: Libraries :: Python Modules',
    # ],
    # extras_require={
    #   'testing': ['pytest'],
    # },
    console=[{'script':'src/craftsmen/__init__.py',}]
)