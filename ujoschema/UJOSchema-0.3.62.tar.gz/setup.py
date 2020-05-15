#
# Copyright (c) 2018-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import setuptools

with open("doc/markdown/ujo-schema.md", "r") as fh:
    long_description = fh.read()

version = '0.3'
try:
    # extend baseversion with buildnumber as microversion forming
    # a version scheme of release.minor.micro
    version = '%s.%s' % (version, os.environ['CI_PIPELINE_IID'])
except BaseException:
    pass

setuptools.setup(
    name="UJOSchema",
    version=version,
    author="Maik Wojcieszak",
    author_email="mw@wobew-systems.com",
    description="UJO Schema is an easy to read and easy"
                "to write language to define UJO data structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.industrial-devops.org",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        "UJOSchema": ["grammar/*.lark"],
    },
    data_files=[
        ("", ["LICENSE"])
    ],
    install_requires=[
        "lark-parser",
        "docopt",
        "ujotypes",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
