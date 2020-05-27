# -*- coding: utf-8 -*-
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import setup

import djangrpc

pipfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pipfile["packages"], r=False)

setup(
    name="djangrpc",
    version=djangrpc.__version__,
    description="Django + Grpc. The Grpc web framework for perfectionists with deadlines.",
    author="Lirian Su",
    author_email="liriansu@gmail.com",
    url="https://github.com/zaihui/djangrpc",
    license="MIT License",
    packages=["djangrpc"],
    install_requires=requirements,
)
