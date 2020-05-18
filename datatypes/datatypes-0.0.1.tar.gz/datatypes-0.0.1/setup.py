#!/usr/bin/env python
from setuptools import setup


name = "datatypes"
kwargs = {"name": name}
kwargs["version"] = "0.0.1"
kwargs["long_description"] = "Coming Soon"
#kwargs["py_modules"] = [name]

setup(
    description=kwargs["long_description"],
    keywords="",
    author='Jay Marcyes',
    author_email='jay@marcyes.com',
    url='http://github.com/Jaymon/{}'.format(name),
    license="MIT",
    classifiers=[ # https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    **kwargs
)
