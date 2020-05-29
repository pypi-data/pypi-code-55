#!/usr/bin/env python3

import os
from datetime import datetime
from setuptools import setup, find_packages

# 0.0.0-dev.* version identifiers for development only (not public)
__version__ = os.environ.get(
    "CI_COMMIT_TAG", "0.0.0.dev" + os.environ.get("CI_JOB_ID", datetime.now().strftime("%Y%m%d")))

setup(
    name="gpg-lite",
    version=__version__,
    license="LGPL3",
    description="python gpg bindings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jaroslaw Surkont, Gerhard Bräunlich, Robin Engler, Christian Ribeaud",
    author_email="jaroslaw.surkont@unibas.ch, "
    "gerhard.braeunlich@id.ethz.ch, "
    "robin.engler@sib.swiss, "
    "christian.ribeaud@karakun.com",
    python_requires=">=3.6",
    install_requires=[
        "dataclasses ; python_version<'3.7'"
    ],
    packages=find_packages(),
    test_suite="test",
)
