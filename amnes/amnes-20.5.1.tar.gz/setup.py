#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""AMNES Setup.py Configuration."""

from setuptools import find_packages, setup

#
# Options
#

LONG_DESCRIPTION = """# Adaptive Meta-Framework for Network Experiment Studies (AMNES)

AMNES is a highly modular tool that aims to simplify the execution of reproducible
network experiments of all kinds.
With its easy configurability, the possibility to develop comprehensive extensions and
the connectivity to different storage backends, this framework helps you to spend less
time on testbed configuration and more time on your network research.

---

_For Usage and Development Guide consult [AMNES Documentation](https://amnes.gitlab.io/amnes/)._
"""

#
# Package
#

setup(
    name="amnes",
    version="20.05.1",
    description="Adaptive Meta-Framework for Network Experiment Studies.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://amnes.gitlab.io/amnes/",
    author="AMNES Project",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://amnes.gitlab.io/amnes/",
        "GitLab.com Source": "https://gitlab.com/amnes/amnes/",
        "Issue Tracker": "https://gitlab.com/amnes/amnes/issues",
    },
    packages=find_packages(where="src"),
    package_dir={"amnes": "src/amnes"},
    package_data={"amnes": ["LICENSE", "THIRDPARTY"]},
    python_requires=">=3.8,<4",
    install_requires=[
        "peewee>=3.13,<4",
        "click>=7.0,<8",
        "pyyaml>=5.3,<6",
        "pyro5<6,>=5.8",
    ],
    extras_require={
        "dev": [
            "pipenv-setup>=3,<4",
            "ptvsd<5,>=4.3",
            "pytest>=5.3,<6",
            "pytest-cov<3,>=2.8",
            "mypy>=0.761",
            "black==19.10b0",
            "isort<5,>=4.3",
            "pylint<3,>=2.4",
            "flake8<3.8,>=3.7",
            "flake8-bugbear>=20.*,<21",
            "pep8-naming<1,>=0.10",
            "flake8-docstrings<2,>=1.5",
            "dlint<1,>=0.10",
            "darglint<2,>=1.2",
            "pdoc3<0.9,>=0.8",
            "mkdocs<2,>=1.1",
            "mkdocs-material>=5.0.*,<5.1",
            "mkdocs-minify-plugin<1,>=0.3.0",
            "pyroma>=2.6,<3",
        ]
    },
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "amnes = amnes.__main__:main",
            "amnes-ctl = amnes.cli.ctl:command",
            "amnes-controller = amnes.cli.controller:command",
            "amnes-worker = amnes.cli.worker:command",
        ]
    },
)
