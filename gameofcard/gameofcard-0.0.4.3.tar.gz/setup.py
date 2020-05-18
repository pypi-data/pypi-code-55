#!/usr/bin/env python3

from setuptools import find_packages, setup

import gameofcard as gc

URL = 'https://github.com/EPgg92/gameofcard/archive/{}'.format(gc.VERSION)

# with open("README.md") as target:
#     long_description = target.read()

setup(
    #     name='gameofcard',
    packages=find_packages(),
    #     version=VERSION,
    #     description='Just a humble implementation of different card games.',
    #     long_description=long_description,
    long_description_content_type='text/markdown',
    #     author='EPgg92',
    #     author_email='poggio.enzo@gmail.com',
    url=URL,
    download_url=URL + '.tar.gz',
    #     keywords=['card', 'game'],
    #     classifiers=["Programming Language :: Python :: 3",
    #                  "Operating System :: OS Independent", ],
)
